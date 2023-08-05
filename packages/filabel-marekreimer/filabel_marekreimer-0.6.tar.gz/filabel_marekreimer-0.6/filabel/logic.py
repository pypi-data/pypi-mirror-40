import enum
import fnmatch
import itertools
import requests
import aiohttp
import asyncio

import sys
class GitHub:
    """
    This class can communicate with the GitHub API
    just give it a token and go.
    """
    API = 'https://api.github.com'

    def __init__(self, token):
        """
        token: GitHub token
        """
        self.token = token
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'filabel'}
        self.session.auth = self._token_auth

    def user(self):
        """
        Get current user authenticated by token
        """
        return self._paginated_json_get(f'{self.API}/user')

    def _token_auth(self, req):
        """
        This alters all our outgoing requests
        """
        req.headers['Authorization'] = 'token ' + self.token
        return req

    def _paginated_json_get(self, url, params=None):
        r = self.session.get(url, params=params)
        r.raise_for_status()
        json = r.json()
        if 'next' in r.links and 'url' in r.links['next']:
            json += self._paginated_json_get(r.links['next']['url'], params)
        return json

    def pull_requests(self, owner, repo, state='open', base=None):
        """
        Get all Pull Requests of a repo

        owner: GtiHub user or org
        repo: repo name
        state: open, closed, all
        base: optional branch the PRs are open for
        """
        params = {'state': state}
        if base is not None:
            params['base'] = base
        url = f'{self.API}/repos/{owner}/{repo}/pulls'
        return self._paginated_json_get(url, params)

    def pr_files(self, owner, repo, number):
        """
        Get files of one Pull Request

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        url = f'{self.API}/repos/{owner}/{repo}/pulls/{number}/files'
        return self._paginated_json_get(url)

    def pr_filenames(self, owner, repo, number):
        """
        Get filenames of one Pull Request. A generator.

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        return (f['filename'] for f in self.pr_files(owner, repo, number))

    def reset_labels(self, owner, repo, number, labels):
        """
        Set's labels for Pull Request. Replaces all existing lables.

        owner: GtiHub user or org
        repo: repo name
        lables: all lables this PR will have
        """
        url = f'{self.API}/repos/{owner}/{repo}/issues/{number}'
        r = self.session.patch(url, json={'labels': labels})
        r.raise_for_status()
        return r.json()['labels']


class AsyncGitHub(GitHub):
    """
    This class can communicate with the GitHub API asynchronnously
    just give it a token and go.
    Other than asynchronnous communication it behaves exactly the same as Github class
    """
    API = 'https://api.github.com'

    def __init__(self, token):
        super().__init__(token)
        self.create_session()
    
    def create_session(self):
        self.session = aiohttp.ClientSession(
            skip_auto_headers=['User-Agent'],
            headers={
                'User-Agent': 'filabel', 
                'Authorization': 'token ' + self.token
            }
        )

    async def user(self):
        """
        Get current user authenticated by token
        """
        return self._paginated_json_get(f'{self.API}/user')

    async def _paginated_json_get(self, url, params=None):
        async with self.session.get(url, params=params) as r:
            json = await r.json()
            r.raise_for_status()
        
        if 'next' in r.links and 'url' in r.links['next']:
            loop = asyncio.get_event_loop()
            t = loop.create_task(self._paginated_json_get(r.links['next']['url'], params))
            await t
            json += t.result()
        
        return json

    async def pr_files(self, owner, repo, number):
        """
        Get files of one Pull Request

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        url = f'{self.API}/repos/{owner}/{repo}/pulls/{number}/files'
        loop = asyncio.get_event_loop()
        t = loop.create_task(self._paginated_json_get(url))
        await t
        return t.result()

    async def pr_filenames(self, owner, repo, number):
        """
        Get filenames of one Pull Request. A generator.

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        loop = asyncio.get_event_loop()
        t = loop.create_task(self.pr_files(owner, repo, number))
        await t
        return (f['filename'] for f in t.result())

    async def reset_labels(self, owner, repo, number, labels):
        url = f'{self.API}/repos/{owner}/{repo}/issues/{number}'

        async with self.session.patch(url, json={'labels': labels}) as r:
            json = await r.json()
            r.raise_for_status()
        return json['labels']

class Change(enum.Enum):
    """
    Enumeration of possible label changes
    """
    ADD = 1
    DELETE = 2
    NONE = 3


class Report:
    """
    Simple container for reporting repo-pr label changes
    """
    def __init__(self, repo):
        self.repo = repo
        self.ok = True
        self.prs = {}


class Filabel:
    """
    Main login of PR labeler
    """
    def __init__(self, token, labels,
                 state='open', base=None, delete_old=True):
        """
        token: GitHub token
        labels: Configuration of labels with globs
        state: State of PR to be (re)labeled
        base: Base branch of PRs to be (re)labeled
        delete_old: If no longer matching labels should be deleted
        asynch: If the connections should be performed asynchronously
        """
        self.github = GitHub(token)
        self.labels = labels
        self.state = state
        self.base = base
        self.delete_old = delete_old

    @property
    def defined_labels(self):
        """
        Set of labels defined in configuration
        """
        return set(self.labels.keys())

    def _matching_labels(self, pr_filenames):
        """
        Find matching labels based on given filenames

        pr_filenames: list of filenames as strings
        """
        labels = set()
        for filename in pr_filenames:
            for label, patterns in self.labels.items():
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        labels.add(label)
                        break
        return labels

    def _compute_labels(self, defined, matching, existing):
        """
        Compute added, remained, deleted, and future label sets

        defined: Set of defined labels in config
        matching: Set of matching labels that should be in PR
        existing: Set of labels that are currently in PR
        """
        added = matching - existing
        remained = matching & existing
        deleted = set()
        future = existing
        if self.delete_old:
            deleted = (existing & defined) - matching
            future = existing - defined
        future = future | matching
        return added, remained, deleted, future

    def run_pr(self, owner, repo, pr_dict):
        """
        Manage labels for single given PR

        owner: Owner of GitHub repository
        repo: Name of GitHub repository
        pr_dict: PR as dict from GitHub API
        """
        pr_filenames = list(
            self.github.pr_filenames(owner, repo, pr_dict['number'])
        )
        added, remained, deleted, future = self._compute_labels(
            self.defined_labels,
            self._matching_labels(pr_filenames),
            set(l['name'] for l in pr_dict['labels'])
        )

        new_labels = self.github.reset_labels(
            owner, repo, pr_dict['number'], list(future)
        )

        new_label_names = set(l['name'] for l in new_labels)
        return sorted(itertools.chain(
            [(a, Change.ADD) for a in added],
            [(r, Change.NONE) for r in remained],
            [(d, Change.DELETE) for d in deleted]
        )) if future == new_label_names else None

    def run_repo(self, reposlug):
        """
        Manage labels for all matching PRs in given repo

        reposlug: Reposlug (full name) of GitHub repo (i.e. "owner/name")
        """
        report = Report(reposlug)
        owner, repo = reposlug.split('/')
        try:
            prs = self.github.pull_requests(owner, repo, self.state, self.base)
        except Exception:
            report.ok = False
            return report

        for pr_dict in prs:
            url = pr_dict.get('html_url', 'unknown')
            report.prs[url] = None
            try:
                report.prs[url] = self.run_pr(owner, repo, pr_dict)
            except Exception:
                pass
        return report

class AsyncFilabel(Filabel):
    def __init__(self, token, labels,
                 state='open', base=None, delete_old=True):
        super().__init__(token, labels, state, base, delete_old)
        self.github = AsyncGitHub(token)
        self.token = token

    async def run_pr(self, owner, repo, pr_dict):
        """
        Manage labels for single given PR asynchronnously

        owner: Owner of GitHub repository
        repo: Name of GitHub repository
        pr_dict: PR as dict from GitHub API
        """
        loop = asyncio.get_event_loop()
        # print("1", file=sys.stderr)
        t = loop.create_task(self.github.pr_filenames(owner, repo, pr_dict['number']))
        await t
        pr_filenames = list(t.result())

        # print("2", file=sys.stderr)

        added, remained, deleted, future = self._compute_labels(
            self.defined_labels,
            self._matching_labels(pr_filenames),
            set(l['name'] for l in pr_dict['labels'])
        )

        # print("3", file=sys.stderr)

        t = loop.create_task(self.github.reset_labels(owner, repo, pr_dict['number'], list(future)))
        await t
        new_labels = t.result()
        # print('New labels:', new_labels)

        # print("4", file=sys.stderr)

        new_label_names = set(l['name'] for l in new_labels)

        return sorted(itertools.chain(
            [(a, Change.ADD) for a in added],
            [(r, Change.NONE) for r in remained],
            [(d, Change.DELETE) for d in deleted]
        )) if future == new_label_names else None

    async def run_repo(self, reposlug):
        """
        Manage labels for all matching PRs in given repo asynchronnously

        reposlug: Reposlug (full name) of GitHub repo (i.e. "owner/name")
        """
        # print("Repo:", reposlug, 'started', file=sys.stderr)
        report = Report(reposlug)
        owner, repo = reposlug.split('/')
        loop = asyncio.get_event_loop()
        try:
            
            task = loop.create_task(self.github.pull_requests(owner, repo, self.state, self.base))
            await task
            prs = task.result()
        except Exception:
            # print('Exception:', e, file=sys.stderr)
            report.ok = False
            return report
        
        tasks = {}
        for pr_dict in prs:
            url = pr_dict.get('html_url', 'unknown')
            report.prs[url] = None
            cr = asyncio.create_task(self.run_pr(owner, repo, pr_dict))
            tasks[url] = cr

        for url, task in tasks.items():
            try:
                await task
                report.prs[url] = task.result()
            except Exception:
                pass

        # print("Repo:", reposlug, 'done', file=sys.stderr)
        return report

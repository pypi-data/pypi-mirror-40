import click
from tqdm import tqdm
from pcloud import PyCloud
from pathlib import Path
import sys
import logging
import configparser


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get_config():

    pth = Path.home() / '.config/pclean.ini'

    if not pth.exists():
        raise FileNotFoundError()

    cp = configparser.ConfigParser()
    cp.read(pth)

    try:
        user = cp['account']['user']
        pwd  = cp['account']['password']
    except KeyError:
        raise

    return user, pwd


def lsr(pc, path = None):
    """
    Retrieves the pCloud filesystem under a given path
    saving all the metadata
    """

    if path is None:
        path = Path('/')

    ds = pc.listfolder(path = path, recursive = True)

    if ds['result'] == 2005:
        raise FileNotFoundError()
    ds['metadata']['full_path'] = path

    folds = [(path, ds['metadata'])]

    while len(folds) > 0:
        cpath, fold = folds.pop(0)

        for f in fold['contents']:
            f['full_path'] = cpath / f['name']
            if f['isfolder']:
                folds.append((f['full_path'], f))

    return ds['metadata']


def hashes(ds):
    """
    Creates a map of hashes to files and folders.
    """

    folds  = [ds]
    hashes = {}
    fmap   = {'files': {}, 'folders': {ds['folderid']: ds}}

    while len(folds) > 0:
        fold = folds.pop(0)

        for f in fold['contents']:
            if f['isfolder']:
                fmap['folders'][f['folderid']] = f
                folds.append(f)
            elif 'hash' in f:
                fmap['files'][f['fileid']] = f
                if f['hash'] not in hashes:
                    hashes[f['hash']] = []
                hashes[f['hash']].append(f)

    return hashes, fmap


def isempty(fold):
    """
    Determines if a folder is empty by checking
    the to_delete flag on each file recursing
    through subdirectories

    Returns a list of file ids and folder ids for
    all "deleted" items or None
    """

    file_ids   = set()
    folder_ids = set()

    for f in fold:
        if f['isfolder']:
            r = isempty(f['contents'])
            if r is None:
                return None

            folder_ids.add(f['folderid'])
            folder_ids.update(r[0])  # Subdirectories that are empty
            file_ids.update(r[1])    # Files that have been deleted
        else:
            if 'to_delete' not in f:
                return None

            file_ids.add(f['fileid'])

    return folder_ids, file_ids


def optimise(ds, fmap, fids):
    """
    Optimises the deletion process by identifying
    where a recursive delete can be used as opposed
    to deleting each file individually
    """

    file_map = fmap['files']
    fold_map = fmap['folders']

    folders = set()
    for fid in fids:
        file_map[fid]['to_delete'] = True
        folders.add(file_map[fid]['parentfolderid'])

    to_delete  = fids.copy()
    empty_fold = set()  # Folders that we have marked as empty

    while len(folders) > 0:
        fold_id = folders.pop()
        empty = isempty(fold_map[fold_id]['contents'])
        if empty is not None:
            empty_fold.difference_update(empty[0])
            folders.difference_update(empty[0])
            to_delete.difference_update(empty[1])
            empty_fold.add(fold_id)

    return empty_fold, to_delete


def delete(pc, fold_del, file_del):

    for fid in tqdm(fold_del, 'deleting folders'):
        pc.deletefolderrecursive(folderid = fid)

    for fid in tqdm(file_del, 'deleting files'):
        pc.deletefile(fileid = fid)


def empty_hash(hashes):
    """
    Determines the hash of an empty file. We do
    this just to be sure that, should they change
    the hashing mechanism, we continue to work.
    """

    for h, groups in hashes.items():
        if groups[0]['size'] == 0:
            return h

    return None


def prune_path(ds, pth):
    """
    Removes a path from a directory
    structure returned by lsr
    """

    new_cwd = ds

    for part in pth.parts[1:]:
        cwd = new_cwd
        for i, f in enumerate(cwd.get('contents', [])):
            if f['name'] == part:
                new_cwd = f
                break
        if new_cwd is None:
            break

    if new_cwd is not None:
        del cwd['contents'][i]


@click.command()
@click.argument('user')
@click.argument('password')
def auth(user, password):

    pth = Path.home() / '.config/pclean.ini'

    cp = configparser.ConfigParser()
    cp['account'] = {
        'user': user,
        'password': password
    }

    with open(pth, 'w+') as f:
        cp.write(f)

    return cp


@click.command()
@click.argument('source')
@click.argument('search', required = False)
@click.option('-n', is_flag = True, help = 'dry run')
@click.option('-v', is_flag = True, help = 'enable logging')
@click.option('-vv', is_flag = True, help = 'more verbose logging')
@click.option('--empty', is_flag = True, help = 'delete empty files, files with size 0')
@click.option('--ignorename', is_flag = True, help = 'delete files even if their names don\'t match')
def clean(source, search, n, v, vv, empty, ignorename):

    try:
        user, pwd = get_config()
    except (FileNotFoundError, KeyError):
        print('use auth to set your username and password')
        sys.exit(1)

    if vv:
        logging.basicConfig(level = logging.DEBUG)
    elif v:
        logging.basicConfig(level = logging.INFO)

    pc = PyCloud(user, pwd)

    source_pth = Path(source)
    search_pth = Path(search) if search is not None else None

    if not source_pth.is_absolute() or \
       (search_pth is not None and not search_pth.is_absolute()):
        print('paths must be absolute')
        sys.exit(1)

    try:
        source_files = lsr(pc, source_pth)
    except FileNotFoundError as e:
        print(f"file not found: {source_pth}")
        sys.exit(1)
    source_hmap, source_fmap = hashes(source_files)

    if not empty:
        # If the empty flag isn't set then we remove
        # any hashes for empty files so they don't
        # match the search set
        eh = empty_hash(source_hmap)
        if eh is not None:
            log.debug('empty file hash: %s', eh)
            del(source_hmap[eh])

    try:
        search_files = lsr(pc, search_pth)
        if search_pth is None:
            # If search isn't specified lsr returns
            # the whole directory tree and we prune
            # out the source path so the whole rest
            # of the tree is searched for duplicates
            prune_path(search_files, source_pth)
    except FileNotFoundError as e:
        print(f"file not found: {search_pth}")
        sys.exit(1)
    search_hmap, search_fmap = hashes(search_files)

    source_fold_id = source_files['folderid']
    search_fold_id = search_files['folderid']

    if source_fold_id == search_fold_id or \
       source_fold_id in search_fmap['folders'] or \
       search_fold_id in source_fmap['folders']:
        print('paths cannot overlap')
        sys.exit(1)

    matches = set(source_hmap.keys()).intersection(set(search_hmap.keys()))

    fids = set()
    if ignorename:
        logging.info('deleting files with matching content')
        for match in matches:
            fids.update(set([x['fileid'] for x in search_hmap[match]]))
    else:
        logging.info('deleting files with matching names and content')
        for match in matches:
            source_names = [x['name'] for x in source_hmap[match]]
            for x in search_hmap[match]:
                if x['name'] in source_names:
                    fids.add(x['fileid'])

    fold_del, file_del = optimise(search_files, search_fmap, fids)

    if n:
        print('Directories to recursively delete')
        for fid in fold_del:
            print(f"    {search_fmap['folders'][fid]['full_path']}")
        print('\nFiles to delete')
        for fid in file_del:
            print(f"    {search_fmap['files'][fid]['full_path']}")

    else:
        delete(pc, fold_del, file_del)


@click.group()
def cli():
    pass


cli.add_command(auth)
cli.add_command(clean)


if __name__ == '__main__':

    cli()

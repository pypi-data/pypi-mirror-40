import os
import hashlib
import pickle
import builtins as __builtin__
import gc


#The dataset archive has size less than below, when dataset save some error may occur.
#And do not use the archive.
minimum_archive_file_size=2000


def prettydataloader(dataloader_func, arg_list, archive_filename, filename_list=None, debug=False):
    """
    Smart dataset loader using dataset archive file.
    If the archive file is fresh, load from the archive instead of reading whole data.
    The "fresh" means that the archive made by below condition.
        - Same data loader function.
        - The args for data loader are same.
        - (Option) Files for dataset are same. Check file modified time and file size.

    Parameters
    ----------
    dataloader_func : function
        Data loader function like below.
          def dataloader(arg_list, hash_check_mode)
            arg_list : Given as second arg for prettydatalader.
            hash_check_mode : If True, must return a part of dataset for calculate
                              data loader's hash for check fresh or not.
                              If False, return whole dataset.
            Returns : Any thing.

    arg_list : any type
        Argument for dataloader_func.

    archive_filename : str
        Store/Load archive pickle filename.

    (Option)filename_list : list of str
        If make dataset using data files, specify the files list.
        Files are checked by file modified time and file size.

    (Option)debug : True/False, default False
        debug print on/off

    Returns
    -------
    dataset : any type
        Dataset return from dataloader_func.

    Examples
    --------
        def dataloader_func(target_line_list, hash_check_mode=False):
            if hash_check_mode==True:
                target_line_list = [target_line_list[0]]
            dataset=[]
            for line in target_line_list:
                filename,label = line.split(' ')
                img = Image.open(filename)
                img = img.resize((2000,1000)).convert('L')
                img = np.asarray(img, dtype='float32')/128.0-1.0
                label = int(label)
                dataset.append( (img,label) )
            return dataset

        ##dataset_list.txt is below.
        ##(img filename) (label)
        #target001.png 1
        #target002.png 1
        #target003.png 2
        #    :
        with open('dataset_list.txt','r') as f:
            target_line_list = f.read().split('\n')
        source_filename_list = [x.split(' ')[0] for x in target_line_list]

        #If dataset_archive.pickle is already exist, below done fast.
        data = prettydataloader(dataloader_func, target_line_list, 'dataset_archive.pickle', filename_list=source_filename_list)
    """

    def print(*arg):
        if debug==True :
            __builtin__.print(*arg)

    now_hash_for_arg_list = hashlib.md5(pickle.dumps(arg_list)).hexdigest()
    now_dataset_for_hash = dataloader_func(arg_list, hash_check_mode=True)
    now_hash_for_data = hashlib.md5(pickle.dumps(now_dataset_for_hash)).hexdigest()
    del now_dataset_for_hash
    print('now_hash_for_arg_list',now_hash_for_arg_list)
    print('now_hash_for_data',now_hash_for_data)
    now_hash_for_file_attribute = None
    if filename_list is not None :
        data=[]
        for target in filename_list:
            temp = os.stat(target)
            data.append((temp.st_size,temp.st_mtime))
        now_hash_for_file_attribute = hashlib.md5(pickle.dumps(data)).hexdigest()
    print('now_hash_for_file_attribute',now_hash_for_file_attribute)

    if os.path.isfile(archive_filename) and os.stat(archive_filename).st_size>=minimum_archive_file_size :
        print('archive file exist. hash check start')
        with open(archive_filename, 'rb') as f:
            dat = pickle.load(f)
        archive_hash_for_arg_list = dat['archive_hash_for_arg_list']
        archive_hash_for_data = dat['archive_hash_for_data']
        archive_hash_for_file_attribute = dat['archive_hash_for_file_attribute']
        archive_dataset = dat['archive_dataset']
        del dat
        print('archive_hash_for_arg_list',archive_hash_for_arg_list)
        print('archive_hash_for_data',archive_hash_for_data)
        print('archive_hash_for_file_attribute',archive_hash_for_file_attribute)

        if (now_hash_for_arg_list == archive_hash_for_arg_list and
            now_hash_for_data == archive_hash_for_data and
            now_hash_for_file_attribute == archive_hash_for_file_attribute) :
            #All checks are OK. can use archive.
            print('same hash. use archive data.')
            return archive_dataset
        else :
            print('different hash. read all target.')
            del archive_hash_for_arg_list
            del archive_hash_for_data
            del archive_dataset

    now_dataset = dataloader_func(arg_list, hash_check_mode=False)

    dic = {}
    dic['archive_hash_for_arg_list']=now_hash_for_arg_list
    dic['archive_hash_for_data']=now_hash_for_data
    dic['archive_dataset']=now_dataset
    dic['archive_hash_for_file_attribute']=now_hash_for_file_attribute

    gc.collect()
    with open(archive_filename, 'wb') as f:
        pickle.dump(dic, f)
    print('pickle write done.')

    return now_dataset

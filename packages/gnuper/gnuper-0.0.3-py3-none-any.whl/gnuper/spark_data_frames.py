"""Contains functions for processing files and (spark) data frames."""

import os  # operating system functions like renaming files and directories
import glob  # pattern matching for paths
from tqdm import tqdm  # progress bar for large tasks
from multiprocessing.pool import ThreadPool  # enables spark multithreading
from functools import partial  # multiprocessing with several arguments


def read_as_sdf(file, sparksession, header=True, inferSchema=True,
                colnames=None, query=None):
    """
    Read in csv file as Spark Data Frame (SDF).
    Optionally change columns and/or run sql query on it.

    Inputs
    ------
    file : Path to the file to be read in.
    sparksession : Sparksession object defined by pyspark.
    header : True if the first row of the csv file represents the header.
    inferSchema : True if the filetype for each column should be inferred.
        Set False if filetypes should simply be kept as string.
    colnames : Array of new column names for the SDF.
    query : String of query which can be executed on read SDF. Should include
        '%(table_name)s' as the origin table, so the newly created SDF is
        being queried.

    Output
    ------
    Spark Data Frame (SDF).
    """
    try:
        sdf = sparksession.read.csv(file,
                                    header=header,
                                    inferSchema=inferSchema)
        if not header:
            if colnames is None:
                print('No header and no column names given... Loading sdf with\
                generic column names (c1, c2, etc.).')
            else:
                sdf = sdf.toDF(*colnames)

        if query is not None:  # execute query if given
            table_name = 'table_'+os.path.splitext(os.path.basename(file))[0]
            sdf.createOrReplaceTempView(table_name)
            sdf = sparksession.sql(query % {'table_name': table_name})

    except Exception as e:
        print('Oops! File:%s cannot be read!' % file)
        sdf = False
    return sdf


def read_alter_save(file, sparksession, header=True, inferSchema=True,
                    colnames=None, query=None,
                    save_path=None, save_format='csv', save_header=True,
                    save_mode='append', save_partition=None):
    """
    Read in a file and potentially alter it with a query.
    Save altered file to a new location with potential partitioning.

    Inputs
    ------

    Reading & Altering:
    --
    file : Path to the file to be read in.
    sparksession : Sparksession object defined by pyspark.
    header : True if the first row of the csv file represents the header.
    inferSchema : True if the filetype for each column should be inferred.
        Set False if filetypes should simply be kept as string.
    colnames : Array of new column names for the SDF.
    query : String of query which can be executed on read SDF. Should include
        '%(table_name)s' as the origin table, so the newly created SDF is
        being queried.

    Saving:
    --
    save_path : Location where altered SDF should be saved to.
    save_format : Format in which the SDF should be saved in (e.g. csv).
    save_header : Boolean if header should be saved as well.
    save_mode : One of two options:
        - 'append' tries to save to save_path if not existing yet
        - 'overwrite' deletes present files before saving
    save_partition : Column which to partition by for saving as separate files.

    Output
    ------
    Simple TRUE statement after successful execution.
    """
    # read in and run potential query on it
    sdf = read_as_sdf(file=file, sparksession=sparksession,
                      header=header, inferSchema=inferSchema,
                      colnames=colnames, query=query)
    # save as desired file split by columns if desired
    sdf.write.save(path=save_path, format=save_format,
                   header=save_header, mode=save_mode,
                   partitionBy=save_partition)
    return True


def union_all(df_list):
    """
    Recursive unioning function.
    Stacking list of SDFs together into one single SDF.

    Inputs
    ------
    df_list : List holding Spark Data Frames with identical schema.

    Output
    ------
    Single SDF which unioned all elements of the input list.
    """
    if len(df_list) > 1:
        return df_list[0].union(union_all(df_list[1:]))
    else:
        return df_list[0]


def sdf_from_folder(folder, attributes, sparksession, file_pattern='*.csv',
                    recursive=False, header=True, inferSchema=True,
                    colnames=None, query=None,
                    save_path=None, save_format='csv', save_header=True,
                    save_mode='append', save_partition=None,
                    action='union'):
    """
    Read several files from a folder into SDFs.
    Afterwards 'union' them, 'save' as altered csvs or 'both'.

    Inputs
    ------

    General:
    --
    attributes : Attributes class with specific options for current run.
    sparksession : Sparksession object defined by pyspark.
    file_pattern :String of pattern of files which should be included
        (e.g. '*.csv').
    recursive : Boolean, if TRUE subdirectories will be included as well.
    action : One of ('union', 'save', 'both') which defines the further
             handling of the files inside the folder after being read.

    Reading & Altering:
    --
    folder : Path to the files to be read in.
    header : True if the first row of the csv file represents the header.
    inferSchema : True if the filetype for each column should be inferred.
        Set False if filetypes should simply be kept as string.
    colnames : Array of new column names for the SDF.
    query : String of query which can be executed on read SDF. Should include
        '%(table_name)s' as the origin table, so the newly created SDF is
        being queried.

    Saving:
    --
    save_path : Location where altered SDF should be saved to.
    save_format : Format in which the SDF should be saved in (e.g. csv).
    save_header : Boolean if header should be saved as well.
    save_mode : One of two options:
        - 'append' tries to save to save_path if not existing yet
        - 'overwrite' deletes present files before saving
    save_partition : Column which to partition by for saving as separate files.

    Output
    ------
    Depending on the input action either a Spark Data Frame ('union' or 'both')
    or a TRUE statement for a successful saving ('save').
    """
    if action not in ('union', 'save', 'both'):
        raise ValueError("Action is not in 'union', 'save' or 'both'... \
        Aborting")

    # get file names
    file_names = glob.glob(folder+file_pattern)
    if recursive:
        subdirs = next(os.walk(folder))[1]
        for d in subdirs:
            file_names.append(glob.glob(folder+d+'/'+file_pattern)[0])

    # if files should be read, altered and saved
    if action in ('save', 'both'):
        pbar = tqdm(total=len(file_names), desc='Read, Alter & Save Files',
                    leave=True)
        for file in file_names:
            read_alter_save(file, sparksession=sparksession,
                            read_header=header,
                            inferSchema=inferSchema,
                            colnames=colnames,
                            query=query, save_path=save_path,
                            save_format=save_format,
                            save_header=save_header,
                            save_mode=save_mode,
                            save_partition=save_partition)
            pbar.update(1)
        print('Files in folder which match pattern have been read,\
              altered & saved!')

    if action in ('union', 'both'):
        # read in files
        raw_df_list = []
        if attributes.mp_flag:
            # assuming 2 threads per processor
            pool = ThreadPool(attributes.n_processors*2)
            for _ in tqdm(pool
                          .imap_unordered(partial(read_as_sdf,
                                                  sparksession=sparksession,
                                                  header=header,
                                                  inferSchema=inferSchema,
                                                  colnames=colnames,
                                                  query=query),
                                          file_names),
                          total=len(file_names), desc='Read Files',
                          leave=True):
                raw_df_list.append(_)
                pass
            pool.close()
        else:
            pbar = tqdm(total=len(file_names), desc='Read Files', leave=True)
            for file in file_names:
                raw_df_list.append(read_as_sdf(file, sparksession=sparksession,
                                               header=header,
                                               inferSchema=inferSchema,
                                               colnames=colnames,
                                               query=query))
                pbar.update(1)

        # unite them
        raw_df = union_all(raw_df_list)
        print('Files have been read and unioned!')
        return raw_df
    return True


def aggregate_chunks(feature_type, attributes, sparksession, unit='antenna_id',
                     create_table=True, cache_table=False, query=None):
    """
    Specific function to aggregate files from chunked folders and run
    aggregation query.

    Inputs
    ------
    feature_type : Type of feature which should be aggregated (e.g. 'hour').
    attributes : Attributes class with specific options for current run.
    sparksession : Sparksession object defined by pyspark.
    unit : Name of column which represents the unit of aggregation.
    create_table : Boolean, if true, table will be created for further
        querying.
    cache_table : Boolean, if true, table will be cached (increases speed if
        table is small enough and is being queried several times).
    query : String of query which can be executed on read SDF. Should include
        '%(table_name)s' as the origin table, so the newly created SDF is
        being queried.

    Output
    ------
    Aggregated spark data frame for chosen feature type.
    """
    # load in all items
    sdf = sdf_from_folder(folder=attributes.antenna_features_path +
                          feature_type+'/',
                          attributes=attributes, sparksession=sparksession,
                          recursive=True)

    # create table
    sdf.createOrReplaceTempView('table_antenna_metrics_'+feature_type+'_df')

    # aggregate
    sdf = sparksession.sql(query)

    if create_table:
        # create aggregated table
        sdf.createOrReplaceTempView('table_'+feature_type)
        # and cache if it will be used more than once
        if cache_table:
            sparksession.catalog.cacheTable('table_'+feature_type)

    print('Aggregated chunks for '+feature_type+'!')

    return sdf

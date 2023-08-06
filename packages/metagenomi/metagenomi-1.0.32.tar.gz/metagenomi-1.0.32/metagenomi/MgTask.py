import boto3
import json
import shlex
import subprocess
import datetime
import doctest
import os
import stat
import pandas as pd
import decimal


from botocore.exceptions import ClientError
from collections import abc
from abc import ABCMeta, abstractmethod
from boto3.dynamodb.conditions import Key, Attr

DBNAME = 'mg-project-metadata'
REGION = 'us-west-2'
TIME_FMT = '%Y-%m-%d %H:%M:%S'

class MgTask:
    def __init__(self, mg_id, d={}):
        # Attributes shared between all MgTask objects
        self.d = d
        self.mg_identifier = mg_id
        self.cmd_run = self.assign('cmd_run')
        self.status = self.assign('status')
        self.jobId = self.assign('jobId')

        self.last_updated = self.assign('updated', type='date')

        self.updated = self.getTime()
        # Everything above is required except self.d
        # is self.d required?
        # req = [attr for attr,value in self.__dict__.items() if attr !='d']

        self.dynamodb = boto3.resource('dynamodb', region_name=REGION)
        self.table = self.dynamodb.Table(DBNAME)

        self.required = []
        self.not_required = ['dynamodb', 'table', 'd', 'not_required',
                            'required', 'last_updated', 'status', 'extras']


    def fix(self):
        # fix 'cmd run'

        missing = self.selfCheck()
        # if 'status' in missing:
        #     # If there are only 3 things missing...
        #     if len(missing) <3 :
        #


        if 'completed' in self.d and 'created' in missing:
            self.created = self.assign('completed', type='date')

        if 'cmds_run' in self.d and 'cmd_run' in missing:
            self.cmd_run = self.assign('cmds_run')



    def checkRequired(self, toWrite):
        for r in self.required:
            if r in toWrite:
                if toWrite[r]:
                    pass
                else:
                    print(f'{r} is None!!')
                    return False
            else:
                print(f'{r} is not even in toWrite')
                return False
        return True




    def selfCheck(self, verbose=False):
        missing = []
        for attr, value in self.__dict__.items():
            if attr in self.required and value is None:
                if verbose: print(f'Attribute {attr} is missing')
                missing.append(attr)
        if len(missing) == 0:
            if verbose: print('')

        return missing


    def getTime(self):
        '''
        Returns current timestamp in human readable format
        '''
        return datetime.datetime.now().strftime(TIME_FMT)


    def assign(self, s, type='str'):
        d = self.d
        if s in d:
            if type=='str':
                try:
                    return str(d[s])
                except ValueError:
                    print(f'Cannot convert {s} to string')
                    return d[s]
            if type=='int':
                no_commas = d[s].replace(',', '')
                try:
                    return int(no_commas)
                except ValueError:
                    print(f'Cannot convert {s} to integer')
                    return no_commas
            if type=='decimal':
                try:
                    return decimal.Decimal(d[s])
                except decimal.InvalidOperation:
                    print(f'Cannot convert {s} to decimal')
                    return d[s]
            if type=='date':
                try:
                    return datetime.datetime.strptime(s, TIME_FMT)
                except ValueError:
                    print(f'Cannot convert {s} to date')
                    return d[s]
            if type=='list':
                if isinstance(d[s], list):
                    return d[s]
                else:
                    print(f'Cannot convert {d[s]} to list')
                    return d[s]

            print(f'Unsure what {s} is')
            return d[s]
        return None

    def run(self):
        # Given the appropriate inputs, run the container
        pass

    def getStatus(self):
        '''
        Difference between this and the next is that this one
        returns the status listed in *this instance of the object*
        and the checkStatus() queries the database to check the
        *actual* status of the underlying DB
        '''

        if 'status' in self.d:
            return d['status']

        return None


    def getFromDynamo(self):
        k = 'mg-identifier'
        v = self.mg_identifier

        response = self.table.query(
                            KeyConditionExpression=Key(k).eq(v)
                            )
        if len(response['Items']) > 1:
            e = f'multiple database entries associated with {v}'
            raise ValueError(e)

        if len(response['Items']) < 1:
            e = f'no database entries associated with {v}'
            print(e)
            return {}

        return response['Items'][0]


    def checkStatus(self, check_discrepancies=True, **kwargs):
        '''
        Queries the database to find the status of the underlying data
        in the database

        Optionally checks if there are any discrepencies between
        the instance and the underlying data
        '''
        # Return status of this task
        # options = Suceeded, Running, Undone, Failed
        # read in what the database holds for the given mg_id

        dynamo_values = self.getFromDynamo()

        if check_discrepancies:
            if self.checkDiscrepencies(dynamo_values, **kwargs):
                return dynamo_values['status']

        if 'status' in dynamo_values: return dynamo_values['status']
        return None


    # def checkDiscrepencies(self, dynamo_values=None, verbose=False):
    #     '''
    #     Will not detect "additional" things in the Dynamo DB not present
    #     in self.d
    #
    #     For example:
    #     >>> s1 = set([(1,2),(2,3)])
    #     >>> s2 = set([(1,2),(2,3),(3,4)])
    #     >>> s1 - s2
    #     set()
    #     '''
    #     if dynamo_values == None:
    #         dynamo_values = self.getFromDynamo()
    #
    #     dynamoValues = self.parseNestedDict(dynamo_values, set())
    #     selfValues = self.parseNestedDict(self.d, set())
    #     diff = selfValues - dynamoValues
    #
    #     return diff


    # def parseNestedDict(self, di, values, verbose=False):
    #     for k,v in di.items():
    #         if isinstance(v, list):
    #             for i in v:
    #                 if isinstance(i, dict):
    #                     self.parseNestedDict(i, values)
    #
    #         elif isinstance(v, dict):
    #             self.parseNestedDict(v, values)
    #             # self.checkDiscrepencies(keys, values)
    #         else:
    #             if isinstance(v, list):
    #                 # print()
    #                 print('V IS A LIST')
    #                 print (k,":",v)
    #             else:
    #                 values.add((k,v))
    #
    #     return (values)

    def writeNew(self, key,value):
        pass


    def writeAppend(self, key, value):
        response = self.table.query(
                            KeyConditionExpression=Key('mg-identifier').eq(self.mg_identifier)
                            )
        # Add to them
        if len(response['Items']) <1:
            raise ValueError(f'{self.mg_identifier} does not exist in DB')

        else:
            if key in response['Items'][0]:
                print(f'{key} is already in the DynamoDB')
                # current = response['Items'][0][key]
                # new_list = current.append()

                result = self.table.update_item(
                    Key={
                        'mg-identifier': self.mg_identifier
                    },
                    UpdateExpression="SET #mg = list_append(#mg, :i)",
                    ExpressionAttributeValues={
                        ':i': [value],
                    },
                    ExpressionAttributeNames = {
                     '#mg': key
                     },
                    ReturnValues="UPDATED_NEW"
                )
                ##
            else:
                print(f'{key} is not in the DynamoDB, adding...')
                result = self.table.update_item(
                    Key={
                        'mg-identifier': self.mg_identifier
                    },
                    UpdateExpression="SET #mg = :i",
                    ExpressionAttributeValues={
                        ':i': [value],
                    },
                    ExpressionAttributeNames = {
                     '#mg': key
                     },
                    ReturnValues="UPDATED_NEW"
                )

    #
    # def write(self, overwrite=True, caution=True):
    #     # Write some important things...
    #     self.updated_at = self.getTime()
    #     diff = self.checkDiscrepencies(dynamo_values = dynamo_values)
    #
    #     if len(diff) == 0:
    #         print('No discrepences!! Write the object')
    #
    #     else:
    #         # If it does not exist already, that's ok
    #         # for d in
    #         pass

            # If it does exist,


        # Query the database to find the object associated with mg_identifier
        # Check if the task already exists for this object
        # If it does, check for discrepencies
        # Write the object, with a new 'updated at' value and any other changed values
        pass


class MgMapping(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)


        self.aligned_mapq_greaterequal_10 = self.assign('aligned_mapq_greaterequal_10', type='int')
        self.aligned_mapq_less_10 = self.assign('aligned_mapq_less_10', type='int')
        self.percent_pairs = self.assign('percent_pairs', type='decimal')

        self.reads_per_sec = self.assign('reads_per_sec', type='int')
        self.seed_size = self.assign('seed_size', type='int')
        self.time_in_aligner_seconds = self.assign('time_in_aligner_seconds', type='int')
        self.too_short_OR_too_many_NNs = self.assign('too_short_OR_too_many_NNs', type='int')
        self.total_bases = self.assign('total_bases', type='int')
        self.total_reads = self.assign('total_reads', type='int')
        self.unaligned = self.assign('unaligned', type='int')

        self.reads_mapped = self.assign('reads_mapped', type='list')
        self.reference = self.assign('reference')

        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]

        self.extras = {k:v for k,v in self.d.items() if k not in self.required and k not in self.not_required}
        # print(self.extras)
    # def write(self):
    #     if self.status == 'submitted':

    def formatToWrite(self):
        '''
        Want it in the format of:
        {'total_bases': '331186490', 'seed_size': '22',
        'total_reads': '133,099,732',
        'aligned_mapq_greaterequal_10': '12,190,844',
        'aligned_mapq_less_10': '19,101',
        'unaligned': '120,749,744',
        'too_short_OR_too_many_NNs': '140,043',
        'percent_pairs': '6.74', 'reads_per_sec': '402,021',
        'time_in_aligner_seconds': '331',
        'reads_mapped':[],
        'ref':s3path,
        'updated':cmd,
        'jobId':jobid,
        }

        '''
        # It's all flat format
        varsDict = vars(self)
        toWrite = {}

        for k,v in varsDict.items():
            if k not in self.not_required:
                toWrite[k] = v

        toWrite.update(self.extras)

        if self.checkRequired(toWrite):
            # print('Yay it passed!')
            return toWrite

        else:
            raise ValueError('Not all requried attributes are present!')


    def write(self):
        '''
        fill in
        '''
        key='mapping'
        value = self.formatToWrite()
        self.writeAppend(key, value)


class MgMapper(MgTask):
    # Made up of multiple MgMappings
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.mappings = []
        for m in self.d:
            self.mappings.append(MgMapping(self.mg_identifier, d=m))
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]


class MgNonpareil(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)

        self.c = self.assign('C', type='decimal')
        self.diversity = self.assign('diversity', type='decimal')
        self.input = self.assign('input')
        self.kappa = self.assign('kappa', type='decimal')
        self.lr = self.assign('LR', type='decimal')
        self.lrstar = self.assign('LRstar', type='decimal')
        self.modelR = self.assign('modelR', type='decimal')
        self.output = self.assign('output')
        self.pdf = self.assign('pdf')
        self.tsv = self.assign('tsv')
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]



class MgAdapterRemoval(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.FTrimmed_reads
        self.KTrimmed_reads
        self.total_removed_reads
        self.trimmed_by_overlap_reads
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]


class MgContaminantRemover(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.contaminants
        self.total_removed_reads
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]

class MgQualityTrimming(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.total_removed_reads
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]


class MgBbmap(MgTask):
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.total_bases = self.assign('total_bases', type='int')
        self.total_reads = self.assign('total_reads', type='int')

        if 'adapter_removal' in d:
            ar = self.d['adapter_removal']
            self.adapter_removal = MgAdapterRemoval(self.mg_identifier, d=ar)
        self.adapter_removal = MgAdapterRemoval(self.mg_identifier, d={})

        if 'contaminant_removal' in d:
            cr = self.d['contaminant_removal']
            self.contaminant_removal = MgContaminantRemover(self.mg_identifier, d=cr)
        self.contaminant_removal = MgContaminantRemover(self.mg_identifier, d={})

        if 'quality_trimming' in d:
            qt = self.d['quality_trimming']
            self.quality_trimming = MgQualityTrimming(self.mg_identifier, d=qt)
        self.quality_trimming = MgQualityTrimming(self.mg_identifier, d={})
        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]




class MgMegahit(MgTask):
    '''
    RULES

    '''
    def __init__(self, mg_id, **kwargs):
        MgTask.__init__(self, mg_id, **kwargs)
        self.avg_sequence_length = self.assign('avg_seq_len', type='decimal')

        # integer
        self.n50 = self.assign('n50', type='int')
        self.seq_params = self.getSequenceParameters()
        self.length_distribution = self.getLengthDistribution()
        self.total_bps = self.assign('total_bps', type='int')
        self.total_seqs = self.assign('total_seqs', type='int')
        self.longest_contig = self.getLongestContig()

        self.required = [attr for attr,value in self.__dict__.items() if attr not in self.not_required]

        # self.tryFill()

        # print('Req in Megahit', self.required)

        # self.required = ['avg_sequence_length', 'length_distribution', 'n50',
        #             'seq_params', 'total_bps', 'total_seqs', 'longest_contig']




    def get_end(self, s):
        ls = s.split('-')

        # Last item in range
        if ls[1] == '':
            return self.getLongestContig()[1]
        else:
            return(int(ls[1]))


    def getLongestContig(self):
        if self.seq_params is not None:
            name =  self.seq_params['length'].idxmax()
            value = self.seq_params['length'][name]
            return (name,value)
        return None


    def getSequenceParameters(self, as_df=True):
        '''
        Return pandas dataframe of top 10 sequences and their parameters
        '''

        if self.assign('Sequence parameters'):
            seqParams = self.d['Sequence parameters']
            if as_df:
                df = pd.DataFrame(seqParams)
                df['length'] = pd.to_numeric(df["length"])
                df['G+C'] = pd.to_numeric(df["G+C"])

                return df
            return seqParams
        return None

    def getLengthDistribution(self, as_df=True):
        '''
        Return pandas dataframe of length distributions
        '''
        if self.assign('Length distribution'):
            ld = self.d['Length distribution']
            if as_df:
                df = pd.DataFrame(ld)
                df['start'] = [int(i.split('-')[0]) for i in df['range']]
                df['end'] = [self.get_end(i) for i in df['range']]

                cols = df.columns
                df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

                df = df.drop(columns=['range'])
                return df
            return length_distributions
        return None


    def fill_self(self):
        item = self.getFromDynamo()
        if 'megahit_metadata' in item:
            self.d = item['megahit_metadata']


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(DBNAME)

    k = 'mg-identifier'
    v = 'HTSP_0078_USA_SRA-assm'

    # response = table.query(
    #                     KeyConditionExpression=Key(k).eq(v)
    #                     )
    # if len(response['Items']) > 1:
    #     e = f'multiple database entries associated with {v}'
    #     raise ValueError(e)
    #
    # r = response['Items'][0]

    md = {'total_bases': '3186490', 'seed_size': '22',
        'total_reads': '133,099,733', 'aligned_mapq_greaterequal_10': '12,190,844',
        'aligned_mapq_less_10': '19,101', 'unaligned': '120,749,744',
        'too_short_OR_too_many_NNs': '140,043', 'percent_pairs': '6.74',
        'reads_per_sec': '402,021', 'time_in_aligner_seconds': '331',
        'jobId':'2a965268-aa93-48c0-9e82-11135688d4a0',
        'test':'YAYAYYAYA'}

    md['cmd_run'] = 'dummy cmd'
    md['reads_mapped'] = ['1', '2']
    md['reference'] = 'ref'

    m = MgMapping(v, d=md)

    m.write()

    # d = m.checkDiscrepencies()
    # print(d)
    # for k,v in zip(d[0], d[1]):
    #     print (k,":",v)
    # m.selfCheck(verbose=True)
    # print(m.d)
    # print(m.mg_identifier)
    # print(m.cmd_run)
    # print(m.mappings[0].mg_identifier)

#
# test()
#
# print('hello')
# t = MgMegahit('PREY_SS21_USA_MGQ-assm')
# print(t)
# print(t.d)


#
# t.fill_self()
#
# t.checkDiscrepencies(verbose=True)



#
#
# t = getTime()
# # type string
# print(type(t))
#
# p = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
# # type datetime.datetime
# print(type(p))







'''

a = MgAssembly(....)

nonpareil = a.getNonpareil()


if nonpareil:
    status = nonpareil.checkStatus()
    if status == 'Undone':
        nonpareil.run()

    if status == 'Complete':
        print(nonpareil)



# WITHIN THE nonpareil container
# run_nonpareil.py

def main():
    # input args

    run_nonpareil()

    md = calculate_metadata()

    # tbl
    #
    # with batch_writer as batch:
    #     batch.put_item({
    #
    #     fhfjpdfnjm
    #     })

    n = MgNonpareil(mg_object='PREY_SS07_MGQ-assm',metadata=md)

    n.write()
'''

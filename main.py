import zySQL as common
import sys

if __name__ == "__main__":
    print(sys.path[0])
    # common.insert('tabletest1', f1='f1', f2='f2').do({
    #     'f1': 'ttttt',
    #     'f2': "rrrrr"
    # })
    # common.update('tabletest1').set(f1='up date test hh').where(f1='1').execute()
    #
    # re = common.select('id', 'f1', 'f2') \
    #     .from_('tabletest1') \
    #     .where(f2='rrrrr') \
    #     .query()
    # print(re)
    # common.delete('tabletest1').execute()
    # re = common.select('id', 'f1', 'f2') \
    #     .from_('tabletest1') \
    #     .query()
    #
    # print(re)

    # common.insert('tabletest1', f1="f1test", f2="f2test").do({
    #     'f1test': '1',
    #     'f2test': '2'
    # })

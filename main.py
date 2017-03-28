import common

if __name__ == "__main__":
    select = common.select()

    re = select.query('tabletest1',
                      f1='22"""w\'ddd\'w',
                      id=1
                      )

    print(re)

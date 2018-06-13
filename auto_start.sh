#!/bin/bash
# This is for auto_learn starting
# Author Ian.Yang
# Creation date 2018-06-13

work_path=$(cd $(dirname $0); pwd)
cd ${work_path}
i=1

startLearn(){
    while [ $i -lt 4 ]
    do
        echo '开始执行自动学习程序';

        check_results=`python ./auto_learn.py 2>&1`
        echo "command(auto_learn.py) results are: $check_results"
        if [[ $check_results =~ "auto_learn_well_down" ]]; then
            echo '第'+ $i + '次运行成功';
            let i+=1;
            startLearn
        else
            echo '程序运行错误，结束！'
            exit 1
        fi
    done
}
startLearn
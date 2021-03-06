#!/bin/bash -x
Cur_Time=`date +%D`
Cur_Y=`echo ${Cur_Time} | cut -d/ -f3`
Cur_M=`echo ${Cur_Time} | cut -d/ -f1`

let Pre_M=Cur_M-1
let L_Pre_M=Pre_M-1
echo ${L_Pre_M}
Pre_Y=${Cur_Y}
L_Pre_Y=${Pre_Y}

if [ ${Pre_M} -eq 0 ]; then
    Pre_M=12
    L_pre_M=11
    let Pre_Y=Cur_Y-1
elif [ ${L_Pre_M} -eq 0 ]; then
    Pre_M=01
    L_Pre_M=12
    let L_Pre_Y=Cur_Y-1
elif [ ${Pre_M} -lt 10 ]; then
    Pre_M=0${Pre_M}
    L_Pre_M=0${L_Pre_M}
elif [ ${Pre_M} -eq 10 ]; then
    L_Pre_M=0${L_Pre_M}
fi

Pre_YM=${Pre_Y}${Pre_M}
Cur_YM=${Cur_Y}${Cur_M}

###btssm_name_varible
FILE="svn_list"
rep_root="https://beisop60.china.nsn-net.net/isource/svnroot"
rep_setup="C_Element/SE_UICA/Setup"

#need to change with different release
rep_installer="lte/fzm/lnz/installer/tags" #TDD FZM
#rep_installer="lte/td/installer/tags" #TDD MACOR

###delete directory of two month before!
echo ${L_Pre_M}
L_Pre_YM=${L_Pre_Y}${L_Pre_M}
echo ${L_Pre_YM}
if [ -d ${L_Pre_YM} ]; then
    rm -rf ./${L_Pre_YM}
    echo "delete ${L_Pre_YM} successful!"
else
    echo "No ${L_Pre_YM} in workspace! So no directory need to delete"
fi


###donwload BTSSM to current directory
rel_branch=("TLF16_BTSSM" "TLF15A_BTSSM" "${Cur_YM}" "${Pre_YM}")
rel_time=("2016" "2015" "${Cur_Y}_${Cur_M}" "${Pre_Y}_${Pre_M}")

for i in ${!rel_branch[@]}; do
    release=${rel_branch[$i]}
    rep_time=${rel_time[$i]}
	list_url="${rep_root}/BTS_D_SE_UI_$rep_time/$rep_installer"
    if [ ! -d ${release} ]; then
	mkdir ${release}
        echo "create directory $release"
    fi
    if [ -d ${release} ]; then
	    cd ./${release}
        if [ -f $FILE ]; then
            rm -f ./$FILE
        fi
        svn list $list_url > svn_list
        cat ${FILE} | awk -F "/" '{print $1}' > ${FILE}
        cat $FILE
        for line in `cat ${FILE}`; do
            build_tag=${line}
            if [ ! -d $build_tag ]; then
                svn co $list_url/$build_tag/$rep_setup/ ./$build_tag/$rep_setup/
                echo "btssm $build_tag download"
            else
                echo "btssm $build_tag alrady exist! skip it!!!!!"
            fi
        done
        cd ..
    fi
done

###Push BTSSM exe to 10.140.90.25
for i in ${!rel_branch[@]}; do
    rsync -avz --exclude=*.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/FZM_TRUNK/${rel_branch[$i]}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/FZM_TRUNK/
done
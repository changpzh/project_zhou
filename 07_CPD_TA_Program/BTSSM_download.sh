#!/bin/bash -x

####time_format
ym=$(date +%y%m)
Cur_Time=`date +%D`
Cur_Y=`echo ${Cur_Time} | cut -d/ -f3`
Cur_M=`echo ${Cur_Time} | cut -d/ -f1`
Cur_YM=${Cur_Y}${Cur_M}

let Pre_M=Cur_M-1
let L_Pre_M=Pre_M-1
echo ${L_Pre_M}
Pre_Y=${Cur_Y}
if [ ${Pre_M} -eq 0 ]; then
    Pre_M=12
    L_pre_M=11
    let Pre_Y=Cur_Y-1
elif [ ${Pre_M} -lt 10 ]; then
    Pre_M=0${Pre_M}
    L_Pre_M=0${L_Pre_M}
elif [ ${Pre_M} -eq 10 ]; then
    L_Pre_M=0${L_Pre_M}
fi

###btssm_name_varible
FILE="./svn_list"
rep_root="https://beisop60.china.nsn-net.net/isource/svnroot"
rep_installer="lte/td/installer/tags"
rep_setup="C_Element/SE_UICA/Setup"

btssm_hea="BTSSiteEM-"
btssm_exe=".exe"

###delete directory of two month before!
L_Pre_Y=${Pre_Y}
L_Pre_YM=${L_Pre_Y}${L_Pre_M}
if [ -d ${L_Pre_YM} ]; then
    rm -rf ./${L_Pre_YM}
    echo "delete ${L_Pre_YM} successful!"
else
    echo "No ${L_Pre_YM} in workspace! So no directory need to delete"
fi

###MACRO Trunk BTSSM get to hzling23
if [ -d ${Cur_YM} ]; then
    cd ./${Cur_YM}
    svn update .
    cd ..
else
    svn co https://beisop60.china.nsn-net.net/isource/svnroot/BTS_D_SE_UI_${Cur_Y}_${Cur_M}/lte/td/installer/tags ./${Cur_Y}${Cur_M}
fi

Pre_YM=${Pre_Y}${Pre_M}
if [ -d ${Pre_YM} ]; then
    cd ./${Pre_YM}
    svn update .
    cd ..
else
    svn co https://beisop60.china.nsn-net.net/isource/svnroot/BTS_D_SE_UI_${Pre_Y}_${Pre_M}/lte/td/installer/tags ./${Pre_Y}${Pre_M}/
fi

###TDD TL16 BTSSM
TL16_B=TL16_BTSSM
if [ -d ${TL16_B} ]; then
    cd ./${TL16_B}
    svn update
    cd ..
else
    svn co https://beisop60.china.nsn-net.net/isource/svnroot/BTS_D_SE_UI_2016/lte/td/installer/tags ./${TL16_B}/

fi

###TDD TL15A BTSSM
TL15A_B=TL15A_BTSSM
if [ -d ${TL15A_B} ]; then
    cd ./${TL15A_B}
    svn update
    cd ..
else
    svn co https://beisop60.china.nsn-net.net/isource/svnroot/BTS_D_SE_UI_2015/lte/td/installer/tags ./${TL15A_B}/
fi

##test for TL16
TL16_B=TL16_BTSSM
if [ -d ${TL16_B} ]; then
    cd ./${TL16_B}
    svn list ${rep_root}/BTS_D_SE_UI_2016/$rep_installer > ${FILE}
	cat ${FILE} | awk -F "/" '{print $1}' > ${FILE}
    for line in `cat ${FILE}`; do
        build_tag=${line}
        if [ ! -d $build_tag ]; then
	        btssm_rel=`echo $line | cut -d_ -f1`
	        btssm_num=`echo $line | awk -F "M_" '{print $2}'`
	        btssm_ver=$btssm_hea$btssm_rel"-"$btssm_num$btssm_exe
            svn export --force $rep_root/BTS_D_SE_UI_2016/$rep_installer/$build_tag/$rep_setup/$btssm_ver ./$build_tag/$rep_setup/
        else
            echo "btssm $build_tag alrady downloaded!"
        fi
    done
fi

##post package to Local PC 10.140.90.25
rsync -avz --exclude=*_000000.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/${Cur_Y}${Cur_M}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/TRUNK/
rsync -avz --exclude=*_000000.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/${Pre_Y}${Pre_M}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/TRUNK/
rsync -avz --exclude=*.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/${TL16A_B}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/BRANCH/
rsync -avz --exclude=*.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/${TL16_B}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/BRANCH/
rsync -avz --exclude=*.bin --exclude=.svn --exclude=*.rpm /lteRel/SC/BTSSM_TDD/${TL15A_B}/* btstest@10.140.90.25:/cygdrive/c/temp/BTSSM_TDD/BRANCH/
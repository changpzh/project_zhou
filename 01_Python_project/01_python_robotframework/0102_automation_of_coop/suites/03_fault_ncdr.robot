*** Settings ***
Documentation    Data checking for fault NCDR
Force Tags        owner-John    Domain-LTE METRIC    phase-AT    phase-Fault    Functionality-Data Checking
Library           coop
Library          OperatingSystem
Library          String
Library          Collections
Variables         ${CURDIR}/../variables/ltemetrics.py
#Suite Setup       Get time

#Test Setup    TC Setup
#Test Teardown      TC Teardown

*** Variables ***
${API_URL}     http://coop.china.nsn-net.net:3000/api/fault_common/pr_data_checking_report_mapping/search/path?type=ncdr&interval=month
${STR_FORMARTED_VIA_INTERVAL}       'STR_YEAR_MONTH'
${NCDR}     NCDR(A&B)
${A_CRI}     A-Critical
${B_MAJ}     B-Major
${C_MIN}     C-Minor
${BASELINE}     Baseline
${NCDR_CUM}     NCDR Cumulative

# PRS == NCDR(A&B)
# PR1 == A-Critical
# PR2 == B-Major
# PR3 == C-Minor

# PRS_B == Baseline
# PRS_C == NCDR Cumulative

*** Test Cases ***
Monthly View for fault Ncdr
    [Tags]      interval-ISOWEEK    type-NCDR
    ${month_data}       Open Web Page And Get Response     ${API_URL}
    # Log     ${month_data.__len__()}
    Check Ltemetrics Api Url and Coop Api Url       ${month_data}


*** Keywords ***
Open Web Page And Get Response
    [arguments]     ${url}
    Open Url    ${url}
    Web Page Can Be Visited
    No JS errors
    ${result}    Get Response Json Result    body
    [return]    ${result}


Web Page Can Be Visited
    Wait Until Page Contains Element Tag Name    body
#    Capture Screenshot

Check Ltemetrics Api Url and Coop Api Url
    [Arguments]     ${data}
    :FOR    ${index}                    IN RANGE                                    ${data.__len__()}

    \       ${ltemetrics_api_url}=      Set Variable                                ${data[${index}]['ltemetrics_api_url']}
    \       ${coop_api_url}=            Set Variable                                ${data[${index}]['coop_api_url']}
    \       Log many                    ${data[${index}]['ltemetrics_url']}         ${data[${index}]['ltemetrics_api_url']}
    \       ...                         ${data[${index}]['ltemetrics_params']}      ${data[${index}]['coop_url']}
    \       ...                         ${data[${index}]['coop_api_url']}           ${data[${index}]['coop_params']}
    \       Run Keyword And Continue On Failure     Should Not Contain      ${coop_api_url}     ignore
    \       Run Keyword If      0==0        Check Response Results    ${ltemetrics_api_url}      ${coop_api_url}
    \       ...                 ${data[${index}]['ltemetrics_url']}     ${data[${index}]['coop_url']}

Check Response Results
    [Arguments]                 ${ltemetrics_api_url}       ${coop_api_url}             ${ltemetrics_url}      ${coop_url}
    ${ltemetrics_results}=      Open Web Page And Get Response          ${ltemetrics_api_url}
    ${coop_results}=            Open Web Page And Get Response          ${coop_api_url}
    @{time_list}=               Get Time List               ${ltemetrics_results}       'STR_YEAR_MONTH'
    :FOR    ${time}     IN      @{time_list}
    \       Get Dictionary from List    ${ltemetrics_results}       'STR_YEAR_MONTH'    ${time}
    \       ${ltemetrics_row_data}=     Set Variable            ${row_data}
    \       Get Dictionary from List    ${coop_results['results']}    'date'    ${time}
    \       ${coop_tmp_row_data}=       Set Variable            ${row_data['stats']}
    \       ${coop_row_data}=           List to Dict            ${coop_tmp_row_data}
    \       ${ncdr_status}=            Get Comparison Status    ${NCDR}        ${ltemetrics_row_data}          PRS      ${coop_row_data['NCDR(A&B)']}
    \       ${a_status}=            Get Comparison status    ${A_CRI}        ${ltemetrics_row_data}            PR1       ${coop_row_data['A-Critical']}
    \       ${b_status}=            Get Comparison Status    ${B_MAJ}        ${ltemetrics_row_data}            PR2      ${coop_row_data['B-Major']}
    \       ${c_status}=            Get Comparison Status    ${C_MIN}        ${ltemetrics_row_data}            PR3      ${coop_row_data['C-Minor']}
    \       ${baseline_status}=            Get Comparison Status    ${BASELINE}        ${ltemetrics_row_data}     PRS_B     ${coop_row_data['Baseline']}
    \       ${ncdr_cum_status}=            Get Comparison Status Special    ${time}     ${NCDR_CUM}        ${ltemetrics_row_data}     PRS_C     ${coop_row_data}        NCDR Cumulative
    \       ${overall status}=          Evaluate    '${ncdr_status}' == 'PASS' and '${b_status}' == 'PASS' and '${c_status}' == 'PASS' and '${baseline_status}' == 'PASS' and '${ncdr_cum_status}' == 'PASS'
    \       Run Keyword And Continue On Failure     Should be True      ${overall status}   Ltemetrics url: ${ltemetrics_url} \n Coop url: ${coop_url} \n Failed on ${time}: \n Name | ltemetrics | coop \n ncdr_status: ${ncdr_status} | ${ltemetrics_row_data['PRS']} | ${coop_row_data['NCDR(A&B)']}\n a_status: ${a_status} | ${ltemetrics_row_data['PR1']} | ${coop_row_data['A-Critical']}\n b_status: ${b_status} | ${ltemetrics_row_data['PR2']} | ${coop_row_data['B-Major']}\n c_status: ${c_status} | ${ltemetrics_row_data['PR3']} | ${coop_row_data['C-Minor']}\n baseline_status: ${baseline_status} | ${ltemetrics_row_data['PRS_B']} | ${coop_row_data['Baseline']}\n ncdr_cum_status: ${ncdr_cum_status} | ${ltemetrics_row_data['PRS_C']} | ${coop_row_data['NCDR Cumulative']}

Get Dictionary from List
    [Arguments]     ${ltemetrics_results}      ${key}       ${time}
    :For            ${index}                   IN RANGE     ${ltemetrics_results.__len__()}
    \               Run Keyword If             '${ltemetrics_results[${index}][${key}]}'=='${time}'     Get Row Data    ${ltemetrics_results[${index}]}

Get Row Data
    [Arguments]     ${row_data}
    Set Test Variable    \${row_data}
    Exit for Loop

Get Time List
    [Arguments]    ${ltemetrics_results}    ${key}
    ${time_list}    Create list
    :FOR    ${index}    IN RANGE    ${ltemetrics_results.__len__()}
    \       Append To List    ${time_list}    ${ltemetrics_results[${index}][${key}]}
    @{time_list}    Set Variable    ${time_list}
    [return]    @{time_list}


*** discarded ***
TC Setup
    ${TC_setup_time}=      Get time

TC Teardown
    ${TC_teardown_time}=    Get time

Get All Report Mappings
    [Arguments]     ${MONTH_API_URL}
    log     ${MONTH_API_URL}
    ${data}=        Get Data From Coop          ${MONTH_API_URL}
    [Return]    ${data}

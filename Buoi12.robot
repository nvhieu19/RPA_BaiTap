*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            https://the-internet.herokuapp.com/login
${BROWSER}        Edge

*** Test Cases ***
Valid Login Test
    [Documentation]    Kiểm tra màn hình xuất hiện nội dung đăng nhập thành công
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    The Internet
    Input Text    id=username    tomsmith
    Input Text    id=password    SuperSecretPassword!
    Click Button    css=button[type="submit"]
    Wait Until Page Contains    You logged into a secure area!
    Close Browser

Invalid Login Test
    [Documentation]    Kiểm tra màn hình đăng nhập thất bại
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    The Internet
    Input Text    id=username    invalid_user
    Input Text    id=password    invalid_pass
    Click Button    css=button[type="submit"]
    Wait Until Page Contains    Your username is invalid!
    Close Browser

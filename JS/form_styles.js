let nameRX = /^[a-zа-яё]+$/i;   // используется в двух функциях


function checkName(name)
{
    let input = document.getElementById('first_name');
    if (name.search(nameRX) == -1 && name != '') 
    {
        input.style.border = '1px solid red';
        input.style.outline = 'none';
        return false
    }
    else 
        if (name == '')
        {
            input.style = 'default';
            return false;
        }
        else
            {
                input.style.border = '1px solid green';
                input.style.outline = 'none';
                return true;
            }
};


function checkSecondName(name)
{
    // фамилии могут быть склеинные (через дефис)
    let secondNameRX = /^(([a-zа-яё]+-)+[a-zа-яё]+)$|^([a-zа-яё]+-{0})$/i;
    let input = document.getElementById('second_name');
    if (name.search(secondNameRX) == -1 && name != '') 
    {
        input.style.border = '1px solid red';
        input.style.outline = 'none';
        return false;
    }
    else 
        if (name == '')
        {
            input.style = 'default';
            return false;
        }
        else
            {
                input.style.border = '1px solid green';
                input.style.outline = 'none';
                return true;
            }
};


function checkPatronomic(name)  // patronomic - отчество
{
    let input = document.getElementById('patronomic');
    if (name.search(nameRX) == -1 && name != '') 
    {
        input.style.border = '1px solid red';
        input.style.outline = 'none';
        return false;
    }
    else 
        if (name == '')
        {
            input.style = 'default';
            return true;
        }
        else
            {
                input.style.border = '1px solid green';
                input.style.outline = 'none';
                return true;
            }
};


function checkNumber(number)
{
    let phoneRX = /^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){11,14}(\s*)?$/;
    let input = document.getElementById('phone');
    if (number.search(phoneRX) == -1 && number != '') 
    {
        input.style.border = '1px solid red';
        input.style.outline = 'none';
        return false;
    }
    else 
        if (number == '')
        {
            input.style = 'default';
            return true;
        }
        else if (number.match(phoneRX)[0] = number)
            {
                input.style.border = '1px solid green';
                input.style.outline = 'none';
                return true;
            }
};


function checkEmail(email)
{
    let emailRX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;


    let input = document.getElementById('email');
    if (email.search(emailRX) == -1 && email != '') 
    {
        input.style.border = '1px solid red';
        input.style.outline = 'none';
        return false;
    }
    else if (email == '')
        {
            input.style = 'default';
            return true;
        }
        else
            {   
                input.style.border = '1px solid green';
                input.style.outline = 'none';
                return true;
            }
};


function checkTextArea(post)
{
    let input = document.getElementById('post');
    if (post == '')
    {
        input.style = 'default';
        return false;
    }
    else if (post.length > 0)
        {
            input.style.border = '1px solid green';
            input.style.outline = 'none';
            return true;
        }
};


function res()
{
    let elements = document.getElementsByTagName("input");
    for (let i = 0; i < elements.length; i++)
        elements[i].style = "default";


    document.getElementsByTagName("textarea")[0].style = "default";
};


function validate()
{
    let first_name = document.forms["postForm"]["first_name"].value;
    let second_name = document.forms["postForm"]["second_name"].value;
    let patronomic = document.forms["postForm"]["patronomic"].value;
    let phone = document.forms["postForm"]["phone"].value;
    let email = document.forms["postForm"]["email"].value;
    let post = document.forms["postForm"]["post"].value;


    if (!checkName(first_name)) return false;
    if (!checkSecondName(second_name)) return false;
    if (!checkTextArea(post)) return false;
    if (!checkPatronomic(patronomic)) return false;
    if (!checkNumber(phone)) return false;
    if (!checkEmail(email)) return false;

    return true;
}




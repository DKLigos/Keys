function show(data) 
{
    let className = "trCity" + data;
    let cities = document.getElementsByClassName(className);
    for (let i = 0; i < cities.length; i++)
    {
        if (cities[i].style.display == 'none')
            cities[i].style.display = 'table-row';
        else
            cities[i].style.display = 'none';
    }
}
function get_regions()
{
    $.ajax({
            type: "POST"
            , url: "http://localhost:8800/cgi-bin/get_regions.py"
            , data: ''
            , dataType: "json"
            , success: function (data)
            {
                html = "<option value='-'>Выберете регион</option>"
                $.each(data, function(i, reg)
                {
                    html += "<option value='" + reg[0] + "'>" + reg[0] + "</option>";
                });
                $("#reg").html(html);
            }
    });
}
function get_cities()
{
    $.ajax({
        type: "POST",
        url: "http://localhost:8800/cgi-bin/get_cities.py",
        data: $("#reg").serialize(),
        dataType: "json",
        success: function (data){
            html = "<option value='-'>Выберете город</option>"
            $.each(data, function(i,city)
            {
                html += "<option value='" + city[0] + "'>" + city[0] + "</option>";
            });
            $("#city").html(html);
        }
    });
}



function get_stat()
{
    $.ajax({
        type: "GET"
        , url: "http://localhost:8800/cgi-bin/get_stat.py"
        , data: ''
        , dataType: "json"
        , success: function(data)
        {
            html = "<tr><th class='headTable' id='statRegHeader'>Регион</th><th class='headTable' id='statCountRegHeader'>Кол-во записей</th></tr>";
            let id = 0   // для создания индивидуальных классов для городов
            $.each(data, function(i, tuple) // tuple - кортеж (связка) вида (reg, [(city1, count_city1), ..., (cityn, count_cityn)])
            {
                id += 1;
                let sum_reg = 0;
                let temp = '';
                $.each(tuple[1], function (i, city)
                {
                    sum_reg += city[1];
                    temp += "<tr class='trCity" + id + "' style='display: none;'><td class='statCity' style='text-indent: 2em;'>" + city[0] + "</td><td class='statCityCount'>" + city[1] + "</tr>";
                });
                html += "<tr class='tdReg'><td class='statReg' onclick='show(" + id + ")'>" + tuple[0] + "</td><td class='statRegCount'>" + sum_reg + "</td></tr>" + temp;
            });
            $("#tableStatReg").html(html);
        }
    });
}

function get_record()
{
    $.ajax({
        type: "GET"
        , url: "http://localhost:8800/cgi-bin/get_records.py"
        , data: ''
        , dataType: "json"
        , success: function(data)
        {
             html = "";
            $.each(data, function(i, comm)
            {

                html += "<div class='statis'><div onclick=Delete("+comm[0]+") class='delete'>X</div><ul><li>Имя: " +comm[1]+ " " +comm[2]+ " " +comm[3]
                + "</li><li>Регион: " +comm[4]
                + "</li><li>Город: " +comm[5]
                + "</li><li>Номер телефона: " +comm[6]
                + "</li><li>email: " +comm[7]
                + "</li><li>Комментарий: " +comm[8] + "</li></ul></div>";
            });
            $("#tableRecord").html(html);
        }
    });
}


function Delete(L)
{

var L;
 $.ajax({
        type: "GET"
        , url: "http://localhost:8800/cgi-bin/delete_post.py"
        , data: {param: L}
        , dataType: "json"
        , success: function()
        {

        }
    });
get_record()
}

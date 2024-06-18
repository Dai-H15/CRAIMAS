const calendar_main = {
    "init":init,
    "get_calendar": get_calendar,
}

function init(url){
    let loading = document.getElementById("loading");
    window.onload = async function get_init_calendar(){
        loading.style = "visibility:visible";
        let contentMonth = document.getElementById("month");
        let contentYear = document.getElementById("year");
        let month = parseInt(document.getElementById("month").textContent);
        let year = parseInt(document.getElementById("year").textContent);
        let table = document.getElementsByTagName("table")[0];
        url = url.replace("month", month).replace("year", year);
        let res = await fetch(url)
        let data = await res.text();
        table.innerHTML = data;
        loading.style = "visibility:hidden";
    }

}
    async function get_calendar(url, to){
        loading.style = "visibility:visible";
        let contentMonth = document.getElementById("month");
        let contentYear = document.getElementById("year");
        let month = parseInt(document.getElementById("month").textContent);
        let year = parseInt(document.getElementById("year").textContent);
        if (to == "n"){
            if(1<= month && month <12){
                month += 1;
            }else{
                month = 1;
                year += 1;
            };
        }else{
            if(1< month && month <=12){
                month -= 1;
        }else{
            month = 12;
            year -= 1;
        }};
        contentMonth.textContent = month;
        contentYear.textContent = year;
        let table = document.getElementsByTagName("table")[0];
        url = url.replace("month", month).replace("year", year);

        let response = await fetch(url);
        let data = await response.text();
        table.innerHTML = data;
        loading.style = "visibility:hidden";
    }

export default calendar_main;
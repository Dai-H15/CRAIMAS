let wind = [];
function open_as_window(url,name,width,height){
    wind.push(window.open(`${url}`, `${name}`, `width=${width},height=${height},toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes`))
};
window.addEventListener('beforeunload', function(){
if (wind.length !=0){
    for(let i = 0; i < wind.length; i++){
        wind[i].close();
    }
}
});

const open_as_window ={
    wind : [],
    "init":init,
    "open_as_window":main,
}
export default open_as_window;

function init(){
    
    window.addEventListener('beforeunload', function(){
    if (open_as_window.wind.length !=0){
        for(let i = 0; i < open_as_window.wind.length; i++){
            open_as_window.wind[i].close();
        }
    }
    });
}
function main(url,name,width,height){
    open_as_window.wind.push(window.open(`${url}`, `${name}`, `width=${width},height=${height},toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes`))
};

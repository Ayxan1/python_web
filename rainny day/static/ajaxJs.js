document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelector('#result').innerHTML='yellow';
  document.querySelector('#form').onsubmit = ()=>{

    const request=new XMLHttpRequest();
    const lat0=document.querySelector('#lat').value;
    const long0=document.querySelector('#long').value;

    lat=(lat0 !=null)?0:lat0;
    long=(long0 !=null)?0:long0;
    request.open('POST', '/ajaxResult');


    request.onload = ()=>{
        const data=JSON.parse(request.responseText);

        if (data.success) {
          document.querySelector('#result').innerHTML=
          '<li>weather summary ------'+data.weather.summary+'</li>'+
          '<li>weather temperature ----'+data.weather.temperatureMin+'</li>'+
          '<li>weather humidity ------ '+data.weather.humidity+'</li>'+
          '<li>weather pressure ------ '+data.weather.pressure+'</li>'+
          '<li>weather windSpeed ------'+data.weather.windSpeed+'</li>'+
          '<li>weather visibility -----'+data.weather.visibility+'</li>';
        }
        else {
          document.querySelector('#result').innerHTML='error occured';
        }

    }
    const data=new FormData();
    data.append('lat',25.92 , 'long', -97.48);
    request.send(data)
    return false;
  }
});

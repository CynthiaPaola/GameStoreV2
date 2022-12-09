function agregarCarrito(){
    var carrito={id_juego:document.getElementById("id").value,
                 cantidad:document.getElementById("cantidad").value};
    var json=JSON.stringify(carrito);
    var url='/carrito/agregar/'+encodeURI(json);
    alert(url);   
    var ajax=new XMLHttpRequest();
    ajax.open("get",url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var mensaje=JSON.parse(this.responseText);
            if(mensaje.estatus=='ok'){
                document.getElementById("notificaciones").style.color="green";
                document.getElementById("notificaciones").innerHTML=mensaje.mensaje;
            }
            else{
                document.getElementById("notificaciones").style.color="red";
                document.getElementById("notificaciones").innerHTML=mensaje.mensaje;
            }
        }
    };
    ajax.send();         
}
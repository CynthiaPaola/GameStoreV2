function eliminarJuego(numJuego){
    res=confirm("¿estas seguro de querer eliminar este juego de su sistema? "+numJuego)
    if(res){
        location.assign("/eliminarJuegos/"+numJuego)
    }
}
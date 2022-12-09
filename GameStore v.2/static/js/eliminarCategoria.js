function eliminarCategoria(numCategoria){
    res=confirm("¿estas seguro de querer eliminar esta categoria de su sistema? "+numCategoria)
    if(res){
        location.assign("/eliminarCategoria/"+numCategoria)
    }
}
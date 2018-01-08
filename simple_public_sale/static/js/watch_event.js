$("#btn-play").click(function () {
    $("#waiting").show();
    $("#event-info").hide();
});

$(document).ready(function () {
    $("#waiting").hide()
    $("#gift-container").hide();
    $(".carousel").carousel();
});
//100000.05
function format_price(value){
    var value = value.toString();
    var len = value.length;


    if(len <= 3){
        return "R$ " + value;
    }
    if(value.charAt(len-3) === "."){
        return format_price(value.substr(0,len-3)).concat(",").concat(value.substr(len-2,3));
    }
    return format_price(value.substr(0,len-3)).concat(".").concat(value.substr(len-3,3));

}

function start_event(json) {
    $("#waiting").hide();
    $("#gift-container").show();


    arrematador = $.parseJSON(json.arrematador_atual);
    movimentos = $.parseJSON(json.movimentos);
    prenda = $.parseJSON(json.prenda);
    tipo_prenda = $.parseJSON(json.prenda_tipo);

    console.log(arrematador);
    console.log(movimentos);
    console.log(prenda[0]);
    console.log(tipo_prenda);


    set_gift_attributes(prenda[0], tipo_prenda[0]);
    set_movements_values(movimentos, arrematador[0]);


    gifts = $.parseJSON(json.prenda.toString());

}

function set_gift_attributes(gift, gift_type) {
    $("#gift-img").attr("src", "/" + gift.fields.url_image);
    $("#gift-title").text(gift_type.fields.nome);

    set_last_move_values("Valor inicial",gift.fields.valor_inicial);

    att1 = $("#attribute-1");
    att1.find("th").text("Descrição");
    att1.find("td").text(gift_type.fields.descricao);
}

function set_movements_values(movements, bidder){
    if(!movements.length){
        console.log("Nenhum movimento feito.");
    }else{
        set_last_move_values(bidder.fields.nome_arrematador,movements[0].fields.valor_arremate);
        if(movements.length > 1){
            $("#move-2").removeClass("invisible");
            set_move_values("#move-2", "lance-2",movements[1].fields.valor_arremate);
        }
        if(movements.length > 2){
            $("#move-2").clone().attr("id","move-3").appendTo("#moves-container");
            set_move_values("#move-3","lance-3", movements[2].fields.valor_arremate);
        }
    }

}

function set_last_move_values(name, value){
    last_move = $("#last-move");
    last_move.find("h1").text(format_price(parseFloat(value).toFixed(2)));
    last_move.find("h2").text(name);
}

function set_move_values(id, name, value){
    last_move = $(id);
    last_move.find("h2").text(name);
    last_move.find("h3").text(format_price(parseFloat(value).toFixed(2)));
}


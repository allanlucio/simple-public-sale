$("#btn-play").click(function () {
    $("#waiting").show();
    $("#event-info").hide();
});

$(document).ready(function () {
    $("#waiting").hide()
    $("#gift-container").hide();
    $(".carousel").carousel();
});

function start_event(json) {
    $("#waiting").hide();
    $("#gift-container").show();


    arrematador = $.parseJSON(json.arrematador_atual);
    movimentos = $.parseJSON(json.movimentos);
    prenda = $.parseJSON(json.prenda);
    tipo_prenda = $.parseJSON(json.prenda_tipo);

    console.log(arrematador);
    console.log("Movimentos: ")
    console.log(movimentos);
    console.log("prenda")
    console.log(prenda[0]);
    console.log(tipo_prenda);


    set_gift_attributes(prenda[0], tipo_prenda[0]);
    set_movements_values(movimentos, arrematador[0]);


    gifts = $.parseJSON(json.prenda.toString());

}

function set_gift_attributes(gift, gift_type) {
    $("#gift-img").attr("src", "/" + gift.fields.url_image);
    $("#gift-title").text(gift_type.fields.nome);

    console.log("OBJETO QUE CHEGOU:" + gift.fields.valor_inicial)
    set_last_move_values("Valor inicial",gift.fields.valor_inicial);

    att1 = $("#attribute-1");
    att1.find("th").text("Descrição");
    att1.find("td").text(gift_type.fields.descricao);
}

function set_movements_values(movements, bidder){
    if(!movements.length){
        console.log("Nenhum movimento feito.");
    }else{
        set_last_move_values(movements[0].fields.arrematador,movements[0].fields.valor);
        if(movements.length > 1){
            $("#move-2").removeClass("invisible");
            set_move_values("#move-2", movements[1].fields.arrematador,movements[1].fields.valor);
        }
        if(movements.length > 2){
            $("#move-2").clone().attr("id","move-3").appendTo("#moves-container");
            set_move_values("#move-3",movements[2].fields.arrematador, movements[2].fields.valor);
        }
    }

}

function set_last_move_values(name, value){
    last_move = $("#last-move");
    num = Number(value);
    console.log("num"+num);
    last_move.find("h1").text(num.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    last_move.find("h2").text(name);
}

function set_move_values(id, name, value){
    last_move = $(id);
    num = Number(value);
    last_move.find("h2").text(name);
    last_move.find("h3").text(num.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}


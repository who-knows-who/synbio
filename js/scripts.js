var headers = ['Type', 'Name', 'Direction', 'Description', 'Remove'];

function openModal(type) {

    var $dialog = $('#dialog_add_part');

    $dialog.dialog("open");
    $dialog.dialog("option", "modal", true);

    var $dialog_part = $('#dialog_part').empty();
    if (type === 'name') {
        $dialog_part.append("Part Name: ").attr('type', 'name')
    } else if (type === 'sequence') {
        $dialog_part.append("Part Sequence: ").attr('type', 'sequence')
    }
    var $part_input = $('<input>').appendTo($dialog_part);
    $part_input.attr('type', 'text').attr('name', 'part');

}

$(document).ready(function() {

    createTable();

    createDialog();

    $("#btn_name").click(function() {
        openModal('name');
    });
    $("#btn_sequence").click(function() {
        openModal('sequence')
    });

    $(window).scroll(move_scroll)

});

function move_scroll(){

    var $container = $('#parts');
    var $table = $('#parts_table');
    var $scroll = $(window).scrollTop();
    var $anchor_top = $table.offset().top;
    var $anchor_bottom = $('#parts_bottom_anchor').offset().top;

    var $clone_table = $('#clone');

    if ($scroll > $anchor_top && $scroll < $anchor_bottom) {


        if ($clone_table.length === 0) {
            $clone_table = $table.clone();
            $clone_table.attr("id", "clone");
            $clone_table.css({
                position: 'fixed',
                'pointer-events': 'none',
                top: 0
            });

            $clone_table.width($table.width());
            $container.append($clone_table);
            $clone_table.find('tbody').css({'visibility': 'hidden'});

        }
    } else {
        $clone_table.remove();
    }
}

function createTable() {

    var $table_head = $('#parts_thead');

    var $tr = $('<tr>').appendTo($table_head);

    for (var i = 0; i < headers.length; i++) {
        var $th = $('<th>').appendTo($tr);
        $th.text(headers[i]);
    }

    $('#parts_tbody').sortable();

}

function createDialog() {

    var $dialog = $('#dialog_add_part');

    $dialog.dialog({
        autoOpen: false,
        modal: true,
        buttons: [
            {
                text: "Cancel",
                click: function() {
                    $(this).dialog("close");
                }

            },
            {
                text: "Add",
                click: function() {
                    addPart();
                    $(this).dialog("close");
                }
            }
        ]

    });
    $dialog.keypress(function(e) {
        if (e.keyCode === $.ui.keyCode.ENTER) {
            addPart();
            $(this).dialog("close");
        }
    });

    var types = [
        {val: "unspecified", text: "Unspecified"},
        {val: "cds", text: "CDS"},
        {val: "promoter", text: "Promoter"},
        {val: "res", text: "Ribosome Entry Site"},
        {val: "terminator", text: "Terminator"}
    ];

    var $dialog_type = $('#dialog_type');
    $dialog_type.attr('id', 'dialog_type').text("Select Part Type: ");

    var $type_select = $('<select>').appendTo($dialog_type);
    $(types).each(function () {
        $type_select.append($("<option>").attr('value', this.val).text(this.text));
    });


    var $dialog_part = $('#dialog_part');
    $dialog_part.attr('id', 'dialog_part');
    // This part filled at runtime (differs between name/sequence)

}
function addPart() {

    var $table_body = $('#parts_tbody');
    var rowCnt = $table_body.find('tr').length;

    var $tr = $('<tr>').appendTo($table_body);

    for (var i = 0; i < headers.length; i++) {

        var $td = $('<td>').appendTo($tr);

        switch (headers[i]) {

            case "Type":
                var $type = $('#dialog_type').find("select option:selected").text();
                $td.append($type);
                //TODO: add symbols to type column
                //TODO: find type of part if unspecified
                break;
            case "Name":
                var $part = $('#dialog_part');
                var name;
                if ($part.attr("type") === "name") {
                    name = $part.find("input").val();
                } else {
                    name = rowCnt.toString();
                    //TODO: find name of part if sequence given
                }
                $td.append(name);
                break;
            case "Direction":
                var $select = $('<select>').appendTo($td);
                $select.append($('<option>').attr("value", "forward").attr("selected", true).text("Forward"));
                $select.append($('<option>').attr("value", "backward").text("Backward"));
                break;
            case "Description":
                var description = "";
                $td.append(description);
                break;
            case "Remove":
                var $remove = $('<button>').attr("type", "button").text("X");
                $remove.click(function () {
                    $(this).parent().parent().remove();
                    //TODO: Make delete row reversible
                });
                $td.append($remove);
                break;
        }
    }

}

var headers = ['Type', 'Name', 'Direction', 'Description', 'Remove'];
var $stack = [];

<<<<<<< HEAD:frontend/js/scripts.js
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

    $("#btn_undo").click(function () {
        undo_delete();
    });

    $(window).scroll(move_scroll)

});

function move_scroll(){

    var $container = $('#parts');
    var $table = $('#parts_table');
    var $scroll = $container.scrollTop();
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
=======
>>>>>>> parent of 72182a0... jQuery sources added to .gitignore:js/scripts.js

function createTable() {

    var table = document.createElement('table');
    table.setAttribute('id', 'partsTable');

    var tableHead = document.createElement('thead');

    var tr = document.createElement('tr');
    tableHead.appendChild(tr);
    table.appendChild(tableHead);

    for (var i = 0; i < headers.length; i++) {
        var th = document.createElement('th');
        th.innerText = headers[i];
        tr.appendChild(th);
    }

    var tableBody = document.createElement('tbody');
    tableBody.setAttribute('id', 'tableBody');
    table.appendChild(tableBody);


    var div = document.getElementById('parts');
    div.appendChild(table);

    $("#sortable").sortable();
    $("#tableBody").sortable();

}

function addPart() {

    var tableBody = document.getElementById('tableBody');
    var rowCnt = document.getElementById('partsTable').rows.length;

    var tr = document.createElement('tr');
    tableBody.appendChild(tr);

    for (var i = 0; i < headers.length; i++) {

        var td = document.createElement('td');
        td = tr.insertCell(i);

        switch(headers[i]) {

<<<<<<< HEAD:frontend/js/scripts.js
            case "Type":
                var $input = $('#dialog_type').find("select option:selected");
                var text = $input.text();
                var val = $input.val();


                switch (val) {
                    case "cds":
                        $td.append('<img src="res/SBOL Visual 1.0.0 PNG/PNG/32x32/cds.png" />');
                        break;
                    case "promoter":
                        $td.append('<img src="res/SBOL Visual 1.0.0 PNG/PNG/32x32/promoter.png" />');
                        break;
                    case "res":
                        $td.append('<img src="res/SBOL Visual 1.0.0 PNG/PNG/32x32/ribosome-entry-site.png" />');
                        break;
                    case "terminator":
                        $td.append('<img src="res/SBOL Visual 1.0.0 PNG/PNG/32x32/terminator.png" />');
                        break;
                }
                $td.append(text);

                //TODO: find type of part if unspecified
=======
            case 'Type':
>>>>>>> parent of 72182a0... jQuery sources added to .gitignore:js/scripts.js
                break;
            case 'Name':
                var text = document.createElement('input');
                text.setAttribute('type', 'text');
                text.setAttribute('value', rowCnt.toString());
                td.appendChild(text);
                break;
            case 'Direction':
                break;
            case 'Description':
                break;
<<<<<<< HEAD:frontend/js/scripts.js
            case "Remove":
                var $remove = $('<button>').attr("type", "button").attr("class", "remove").text("X");
                $remove.click(function () {
                    var $row = $(this).parent().parent();
                    $stack.push($row);
                    $row.remove();
                });
                $td.append($remove);
=======
            case 'Remove':
                var button = document.createElement('input');
                button.setAttribute('type', 'button');
                button.setAttribute('value', 'Remove');
                button.setAttribute('onClick', 'removeRow(this)');
                td.appendChild(button);
>>>>>>> parent of 72182a0... jQuery sources added to .gitignore:js/scripts.js
                break;
        }
    }

}

<<<<<<< HEAD:frontend/js/scripts.js
function undo_delete() {

    var $table_body = $('#parts_tbody');

    var $row = $stack.pop();

    switch ($row) {

        case undefined:
            alert("No more deletions to undo!");
            break;
        default:
            $table_body.append($row);
            $row.find('.remove').click(function () {
                var $row = $(this).parent().parent();
                $stack.push($row);
                $row.remove();
            });
            break;
    }
=======
function removeRow(oButton) {

    var table = document.getElementById('partsTable');
    table.deleteRow(oButton.parentNode.parentNode.rowIndex);

>>>>>>> parent of 72182a0... jQuery sources added to .gitignore:js/scripts.js
}

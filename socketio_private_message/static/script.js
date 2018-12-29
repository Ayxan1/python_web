$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5000');

    var socket_messages = io('http://127.0.0.1:5000/messages')
    var current_user='';
    var private_socket = io('http://127.0.0.1:5000/private')
    var groupName='';

////////////////////// time  /////////////////////////////
const now = new Date();
console.log(now);
///////////////////////////////////////////////////



///////////////////   Login    /////////////////////////////

        $('#send_username').on('click', function() {
            current_user=$('#username').val();
            private_socket.emit('username', $('#username').val());
        });

        private_socket.on('username added', function(msg){
            document.querySelector('#logginedUser').innerHTML=msg;
            document.querySelector('#group_area').style.display='block';
        });



/////////////////////session autocomplete //////////////


        private_socket.emit('autoUsername', 'sdasd');
        private_socket.on('auto_username added', function(msg){
            document.querySelector('#logginedUser').innerHTML=msg.message;
            current_user=msg.message;
            if (msg.message!='not logged in') {
                document.querySelector('#group_area').style.display='block';
            }
        });

////////////////////////////////////////////////






///////////////////////////////  auto connection to current group  ////////////////////////////////////////////////


  kind='auto'
  private_socket.emit('joiningToRoom', {'roomname': groupName, 'kind' : kind});
  private_socket.on('previousMessages', function(msg) {
    if (msg['showBlock']=='yes') {
        document.querySelector('#group_messaging_form').style.display='block';
        var myList = document.getElementById('listGroup');
        myList.innerHTML = '';
        document.querySelector('#logginedGroup').innerHTML=msg['currentRoomName'];
    for (var i = 0; i < msg['previous_messages'].length && i<=100 ; i++) {
      const li = document.createElement('li');
      li.innerHTML = msg['previous_messages'][i];
      document.querySelector('#listGroup').append(li);
    }

  }

  });





///////////////////////////////////////////////////////////////////////////////












////////////////////////////////////////////////



//////////////////////     Previous global messaging   //////////////////////////
    $('#send').on('click', function() {
        var message = $('#message').val();
        var person =current_user;
        socket_messages.emit('message from user', {'username' : person, 'message' : message});

    });

    socket_messages.on('from flask', function(msg) {
      const li = document.createElement('li');
      li.innerHTML = `sended message: ${msg.message} by ${msg.username}`;
      document.querySelector('#list').append(li);

    });
////////////////////////////////////////////////





////////////////////////  socket origination  ////////////////////////
    socket.on('server orginated', function(msg) {
        alert(msg);
    });
////////////////////////////////////////////////










////////////////// Private messaging //////////////////////////////


    $('#send_private_message').on('click', function() {
        var recipient = $('#send_to_username').val();
        var message_to_send = $('#private_message').val();
        private_socket.emit('private_message', {'username' : recipient, 'message' : message_to_send, 'from_whom' : current_user});
    });

    private_socket.on('new_private_message', function(msg) {
      const li = document.createElement('li');
      li.innerHTML = `sended message: ${msg.message} by ${msg['sended by']}`;
      document.querySelector('#listPrivate').append(li);
    });

////////////////////////////////////////////////



/////////////////// Show group list /////////////////////////////

  private_socket.emit('show_groups', {'message': 'ss'});
  private_socket.on('group_list', function(groups) {
    for (var i = 0; i < groups.length; i++) {
      const option = document.createElement('option');
      option.innerHTML = groups[i];
      document.querySelector('#groupList').append(option);
    }
  });
  document.querySelector('#groupList').style.display='block';
  document.querySelector('#joinThisGroup').style.display='block';
/////////////////////////////////////////////////////////////////

/////////////////////////////// joining to room /////////////////////
$('#joinThisGroup').on('click', function() {
  groupName=document.querySelector('#groupList').value;
  kind='manual'
  console.log('jointhisgroup buttonuna basildi');
  private_socket.emit('joiningToRoom', {'roomname': groupName, 'kind' : kind});
  document.querySelector('#group_messaging_form').style.display='block';
  private_socket.on('previousMessages', function(msg) {
    var myList = document.getElementById('listGroup');
    myList.innerHTML = '';
    document.querySelector('#logginedGroup').innerHTML=msg['currentRoomName'];
    for (var i = 0; i < msg['previous_messages'].length && i<=100 ; i++) {
      const li = document.createElement('li');
      li.innerHTML = msg['previous_messages'][i];
      document.querySelector('#listGroup').append(li);
    }

  });
});
/////////////////////////////////////////////////////////////////////

//############## taking previous messages #####################




////////////////////////////////////////////////




/////////////////////       Group messaging        /////////////
$('#group1').on('click', function() {
    var message_to_send = $('#group_message').val();
    const now = new Date();
    private_socket.emit('group_messaging', {'message' : message_to_send, 'from_whom' : current_user, 'group_name' : groupName, 'time' : now});
}); /////// emitin ici ++

private_socket.on('new_group_message', function(msg) {
  const li = document.createElement('li');
  li.innerHTML = `sended message: ${msg.message} by ___ ${msg['sended by']} in _____ ${msg['time']}`; ///html ici++
  document.querySelector('#listGroup').append(li);
});

//////////////////////////////////


//////////////////Add new group ///////////////////////////////

$('#newGroupNameAdd').on('click', function() {
    var groupName = $('#newGroupName').val();
    private_socket.emit('addNewGroup', groupName);
    private_socket.on('permission',function(msg){
      permis=msg.message

    console.log('add butonu clicklendi'+'permis -----  '+permis);

    if (permis=='add') {
      document.querySelector('#alertConflictGroupName').style.display='none';
      console.log('display: nona   a girdi');
      const option = document.createElement('option');
      option.innerHTML = groupName;
      document.querySelector('#groupList').append(option);
    }else if(permis=='not add'){
      document.querySelector('#alertConflictGroupName').style.display='block';
    }

    });
});





///////////////////////////////////////////////////////////////
    /*

    socket.on('connect', function() {

        socket.send('I am now connected!');

        socket.emit('custom event', {'name' : 'Anthony'});

        socket.on('from flask', function(msg) {
            alert(msg['extension']);
        });

        socket.on('message', function(msg) {
            alert(msg);
        });

    });

    */

});

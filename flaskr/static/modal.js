var $j = jQuery.noConflict();

function openProductAddModal() {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/add_product',
    type: 'GET',
    success: function(data) {
      // Populate modal content with returned HTML
      $('#productModal .modal-content').html(data);
      // Show modal
      $('#productModal').modal('show');
    }
  });
}

function openProductEditModal(id) {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/edit_product/'+id,
    type: 'GET',
    data: {productid: id},
    success: function(data) {
      // Populate modal content with returned HTML
      $('#productModal .modal-content').html(data);
      $('#productModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#productModal').modal('show');
    }
  });
}

function openCustomerOrderModal(id) {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/customerOrder/'+id,
    type: 'GET',
    data: {productid: id},
    success: function(data) {
      // Populate modal content with returned HTML
      $('#productModal .modal-content').html(data);
      $('#productModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#productModal').modal('show');
    }
  });
}

function openOrderModal(id) {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/viewOrder/'+id,
    type: 'GET',
    data: {orderid: id},
    success: function(data) {
      // Populate modal content with returned HTML
      $('#orderModal .modal-content').html(data);
      $('#orderModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#orderModal').modal('show');
    }
  });
}

function openMyOrderModal(id) {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/viewmyorder/'+id,
    type: 'GET',
    data: {orderid: id},
    success: function(data) {
      // Populate modal content with returned HTML
      $('#myOrderModal .modal-content').html(data);
      $('#myOrderModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#myOrderModal').modal('show');
    }
  });
}

function openAddWorkerModal() {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/add_worker',
    type: 'GET',
    success: function(data) {
      // Populate modal content with returned HTML
      $('#dashModal .modal-content').html(data);
      $('#dashModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#dashModal').modal('show');
    }
  });
}

function openOrdelModal(id) {
  // Make AJAX request to Flask route to get modal HTML
  $j.ajax({
    url: '/viewOrdel/'+id,
    type: 'GET',
    data: {orderid: id},
    success: function(data) {
      // Populate modal content with returned HTML
      $('#ordelModal .modal-content').html(data);
      $('#ordelModal .modal-content').append(data.htmlresponse);
      // Show modal
      $('#ordelModal').modal('show');
    }
  });
}
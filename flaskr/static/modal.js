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
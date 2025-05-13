// Get all input elements of type text
var textInputs = document.querySelectorAll('input[type="text"]');

// Attach the event listener to each text input
textInputs.forEach(function(input) {
  input.addEventListener('input', function() {
    // Limit the input length to 30 characters
    if (this.value.length > 30) {
      this.value = this.value.slice(0, 30);
    }
  });
});
//local store
document.addEventListener("DOMContentLoaded", function () {
    // Array of tag IDs
    const tagIds = ["position_label", "legend_title", "legend_title_size", "legend_title_weight", "legend_Title_color", "legend_text_color", "legend_opacity", "legend_box_style", "legend_box_size", "face_color_legend", "edge_color_legend", "legend_line_style", "legend_line_width", "layout_axis_spines","Plot_bg_color", "layout_theme_style", "layout_xtick_color", "layout_ytick_color", "layout_xlabel_title", "layout_xlabel_color", "layout_xlabel_background_color", "layout_xlabel_border_color", "layout_xlabel_box_style", "layout_xlabel_Box_Style_pad", "layout_ylabel_title", "layout_ylabel_color", "layout_ylabel_background_color", "layout_ylabel_border_color", "layout_ylabel_box_style", "layout_ylabel_Box_Style_pad", "layout_plot_title", "layout_title_color", "layout_title_background_color", "layout_title_border_color", "layout_title_box_style", "layout_title_Box_Style_pad", "marker_color", "marker_size","marker_line_width", "marker_categorization", "marker_palette", "marker_alpha", "marker_edge_colors"];
    // Loop through each tag
    tagIds.forEach(tagId => {
        const tagElement = document.getElementById(tagId);
        // Check if the element exists
        if (!tagElement) {
            console.error(`Element with ID '${tagId}' not found.`);
            return;  // Skip to the next iteration if the element is not found
        }
        // Check if a stored value exists in local storage
        const storedValue = localStorage.getItem(tagId);
        // Set the tag value based on the stored value
        if (storedValue) {
            if (tagElement.tagName === 'INPUT' || tagElement.tagName === 'SELECT') {
                tagElement.value = storedValue;
            } else {
                tagElement.innerText = storedValue;
            }
        }
        // Add an event listener to save the tag value to local storage when it changes
        tagElement.addEventListener("input", function () {
            const value = (tagElement.tagName === 'INPUT' || tagElement.tagName === 'SELECT') ? tagElement.value : tagElement.innerText;
            localStorage.setItem(tagId, value);
        });
    });
});

function downloadImage(imageId , num) {
    var imgSrc = document.getElementById(imageId).src;
    var a = document.createElement('a');
    a.href = imgSrc;
    console.log(num)
    a.download = 'downloaded_image_'+num+'.jpg' // You can customize the downloaded filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
function sendImage(imageid) {
    // Get the image source
    var imageSource = document.getElementById(imageid).getAttribute('src');
    //// Store the image source in sessionStorage (you can use other methods like cookies, local storage, etc.)
    sessionStorage.setItem('sharedImage', imageSource);
}
function sendImage1(img){
    console.log(img, "lllllllll")
}


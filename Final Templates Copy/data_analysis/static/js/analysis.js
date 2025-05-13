document.addEventListener("DOMContentLoaded", function () {
    // Get the select element
    
    const selectElement = document.getElementById("mySelect");

    // Check if a stored option exists in local storage
    const storedOption = localStorage.getItem("selectedOption");

    // Set the selected option based on the stored value
    if (storedOption) {
        selectElement.value = storedOption;
        displaySelectedOption(storedOption);
    }

    // Add an event listener to save the selected option to local storage when it changes
    selectElement.addEventListener("change", function () {
        localStorage.setItem("selectedOption", selectElement.value);
        displaySelectedOption(selectElement.value);
    });
});



function displaySelectedOption(selectedOption) {
    //one_data
    const thisDataMax = document.getElementById("max");
    const thisDataMin = document.getElementById("min");
    const thisDataSum = document.getElementById("sum");
    const thisDataCount = document.getElementById("count");
    const thisDataMean = document.getElementById("mean");
    const thisDataMedian = document.getElementById("median");
    const thisDatanunique = document.getElementById("nunique");
    const thisDatamode = document.getElementById("mode");
    const thisDatastd = document.getElementById("std");
    const thisDataprod = document.getElementById("prod");
    const thisDataidxmax = document.getElementById("idxmax");
    const thisDataidxmin = document.getElementById("idxmin");
   //table_data
    const the_operation = document.getElementById("operation");
    const the_describe = document.getElementById("describe");
    const the_drop = document.getElementById("drop");
    const the_dropna = document.getElementById("dropna");
    const the_head = document.getElementById("head");
    const the_tail = document.getElementById("tail");
    const the_sort = document.getElementById("sort");
    const the_rename = document.getElementById("rename");

    const the_pivot = document.getElementById("pivot");
    const the_fillna = document.getElementById("fillna");
    const the_replace = document.getElementById("replace");
    const the_column_update = document.getElementById("column_update");
    const the_operations_on_columns = document.getElementById("operations_on_columns");
    const the_duplicated = document.getElementById("duplicated");
    const the_drop_duplicates = document.getElementById("drop_duplicates");
    const the_cross_tabulation = document.getElementById("cross_tabulation");
    const the_stacking_and_unstacking = document.getElementById("stacking_and_unstacking");
    const the_cumulative_sum = document.getElementById("cumulative_sum");
    const the_cumulative_product = document.getElementById("cumulative_product");
    const the_cumulative_maximum = document.getElementById("cumulative_maximum");
    const the_cumulative_minimum = document.getElementById("cumulative_minimum");
    const the_delete_row = document.getElementById("delete_row");
    const the_rename_column = document.getElementById("rename_column");
    const the_column_copy = document.getElementById("column_copy");
    const the_group_by = document.getElementById("group_by");
    
    
    
    const the_sql_query = document.getElementById("sql_query");
    const container_item_2 = document.getElementById("container_item_2_id");
    const join_table = document.getElementById("join_table");
    
    
    const elementsToHide = [
        thisDataMax, thisDataMin, thisDataSum,thisDataCount,thisDataMedian, thisDataMean,thisDatanunique,
        thisDatamode,thisDatastd,thisDataprod,thisDataidxmax,thisDataidxmin, the_operation,the_describe, 
        the_drop,the_dropna, the_head, the_tail, the_sort, the_rename,the_pivot, the_fillna, the_replace, 
        the_column_update, the_operations_on_columns, the_duplicated, the_drop_duplicates, the_cross_tabulation, 
        the_stacking_and_unstacking, the_cumulative_sum, the_cumulative_product,the_cumulative_maximum, the_cumulative_minimum,
        the_delete_row, the_rename_column, the_column_copy, the_group_by,the_sql_query, container_item_2, join_table
      ];
      
      elementsToHide.forEach(element => {
        element.style.display = "none";
      });
      


    if (selectedOption === "max") {
        thisDataMax.style.display = "block";
    } else if (selectedOption === "min") {
        thisDataMin.style.display = "block";
    } else if (selectedOption === "sum"){
        thisDataSum.style.display = "block";
    }else if (selectedOption === "count"){
        thisDataCount.style.display = "block";
    }else if (selectedOption === "mean"){
        thisDataMean.style.display = "block";
    }else if (selectedOption === "median"){
        thisDataMedian.style.display = "block";
    }else if (selectedOption === "nunique"){
        thisDatanunique.style.display = "block";
    }else if (selectedOption === "mode"){
        thisDatamode.style.display = "block";
    }else if (selectedOption === "std"){
        thisDatastd.style.display = "block";
    }else if (selectedOption === "prod"){
        thisDataprod.style.display = "block";
    }else if (selectedOption === "idxmax"){
        thisDataidxmax.style.display = "block";
    }else if (selectedOption === "idxmin"){
        thisDataidxmin.style.display = "block";
    }else if (selectedOption === "operation"){
        the_operation.style.display = "block";
    }else if (selectedOption === "describe"){
        the_describe.style.display = "block";
    }else if (selectedOption === "drop"){
        the_drop.style.display = "block";
    }else if (selectedOption === "dropna"){
        the_dropna.style.display = "block";
    }else if (selectedOption === "head"){
         the_head.style.display = "block";
    }else if (selectedOption === "tail"){
         the_tail.style.display = "block";
    }else if (selectedOption === "sort"){
         the_sort.style.display = "block";
    }else if (selectedOption === "rename"){
         the_rename.style.display = "block";
    }else if (selectedOption === "pivot"){
        the_pivot.style.display = "block";
    }else if (selectedOption === "fillna"){
        the_fillna.style.display = "block";
    }else if (selectedOption === "replace"){
        the_replace.style.display = "block";
    }else if (selectedOption === "column_update"){
        the_column_update.style.display = "block";
    }else if (selectedOption === "operations_on_columns"){
        the_operations_on_columns.style.display = "block";
    }else if (selectedOption === "duplicated"){
        the_duplicated.style.display = "block";
    }else if (selectedOption === "drop_duplicates"){
        the_drop_duplicates.style.display = "block";
    }else if (selectedOption === "cross_tabulation"){
        the_cross_tabulation.style.display = "block";
    }else if (selectedOption === "stacking_and_unstacking"){
        the_stacking_and_unstacking.style.display = "block";
    }else if (selectedOption === "cumulative_sum"){
        the_cumulative_sum.style.display = "block";
    }else if (selectedOption === "cumulative_product"){
        the_cumulative_product.style.display = "block";
    }else if (selectedOption === "cumulative_maximum"){
        the_cumulative_maximum.style.display = "block";
    }else if (selectedOption === "cumulative_minimum"){
        the_cumulative_minimum.style.display = "block";
    }else if (selectedOption === "delete_row"){
        the_delete_row.style.display = "block";
    }else if (selectedOption === "rename_column"){
        the_rename_column.style.display = "block";
    }else if (selectedOption === "column_copy"){
        the_column_copy.style.display = "block";
    }else if (selectedOption === "group_by"){
        the_group_by.style.display = "block";
    }else if (selectedOption === "sql_query") {
        the_sql_query.style.display = "block";
    } else if (selectedOption === "join"){
        container_item_2.style.display = "block"
        join_table.style.display = "block"
    } 
}
// The hide python flask element
var selectOption = document.getElementsByName('select_option')[0];
var valueDiv = document.getElementById('value-div');

selectOption.addEventListener('change', function() {
    
    valueDiv.style.display = 'none';
});
 
    function validateInput() {
        // Get the input value
        var inputValue = document.getElementById("selected_column_name").value;
        const error_inputValue = document.getElementById("error-message")

        // Check if the input value is less than 2 characters
        if (inputValue.length < 2) {
            // Display an error message
            error_inputValue.innerHTML = "Error: Input must be at least 2 characters long.";
            error_inputValue.style.display = "block"
            // Prevent the form from being submitted
            return false;
        } else {
            // Clear the error message if the input is valid
            error_inputValue.innerHTML = "";
            // Allow the form to be submitted
            return true;
        }
    }


 // Initialize CodeMirror color apply on sql query
 document.addEventListener("DOMContentLoaded", function() {
    const sqlEditor = CodeMirror.fromTextArea(document.getElementById("input_Field"), {
      mode: "text/x-sql",
      lineNumbers: false,
      theme: "default",
    });
  });
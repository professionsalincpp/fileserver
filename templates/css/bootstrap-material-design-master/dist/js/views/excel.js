function processMergedCells(data, merges) {
  const result = [];
  for (let i = 0; i < data.length; i++) {
    const row = [];
    for (let j = 0; j < data[i].length; j++) {
      const cellValue = data[i][j];
      if (cellValue !== null && cellValue !== undefined) {
        const mergeInfo = getMerge(merges, i, j);
        if (mergeInfo && isTopLeft(mergeInfo, i, j)) {
          row.push({
            value: cellValue,
            rowspan: mergeInfo.e.r - mergeInfo.s.r + 1,
            colspan: mergeInfo.e.c - mergeInfo.s.c + 1,
          });
        } else {
          row.push({
            value: cellValue,
            rowspan: 1,
            colspan: 1,
          });
        }
      } else if (isInMerge(merges, i, j)) {
        console.log("skipping");
      } 
    }
    result.push(row);
  }
  return result;
}

function isTopLeft(merge, row, col) {
    return row === merge.s.r && col === merge.s.c;
}

function isInMerge(merge, row, col) {
  if (!merge) {
      return false;
  }
  for (const m of merge) {
    if (m.s.r <= row && row <= m.e.r && m.s.c <= col && col <= m.e.c) {
      return true;
    }
  }
  return false;
}

function getMerge(merges, row, col) {
    if (!merges) {
      return null;
    }

    for (const merge of merges) {
        if (merge.s.r <= row && row <= merge.e.r && merge.s.c <= col && col <= merge.e.c) {
            return merge;
        }   
    }
    return null;
}
function displayJsonXlsx(json_data, worksheet) {
    try {
        let table = document.createElement("table");
        let table_body = document.createElement("tbody");
        let table_head = document.createElement("thead");
        let table_head_row = document.createElement("tr");
        const table_width = Math.max.apply(null, json_data.map(function(o) { return Object.keys(o).length; }));
        let lettersmap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        let blank_cell = document.createElement("th");
        table_head_row.appendChild(blank_cell);
        blank_cell.className = "excel-table-numeration-cell";
        for (let i = 0; i < table_width; i++) {
            let table_head_cell = document.createElement("th");
            table_head_cell.className = "excel-table-head-cell";
            if (i > 25) {
                // Set text alignment to center
                table_head_cell.innerText = lettersmap[Math.floor(i / 26)] + lettersmap[i % 26];
            }
            table_head_cell.innerText = lettersmap[i];
            table_head_row.appendChild(table_head_cell);
        }
        table_head.appendChild(table_head_row);
        table_head_row = document.createElement("tr");
        table_head.appendChild(table_head_row);
        table.appendChild(table_head);
        table.appendChild(table_body);
        for (let i = 0; i < json_data.length; i++) {
            let table_row = document.createElement("tr");
            let number_cell = document.createElement("td");
            number_cell.innerText = i + 1;
            number_cell.className = "excel-table-numeration-cell";
            table_row.appendChild(number_cell);
            let column = 0;
            for (let j = 0; j < Object.keys(json_data[i]).length; j++) {
                let table_cell = document.createElement("td");
                // table_cell.rowSpan = json_data[i][Object.keys(json_data[i])[j]["colspan"]];
                // table_cell.colSpan = json_data[i][Object.keys(json_data[i])[j]["rowspan"]];
                let element = json_data[i][Object.keys(json_data[i])[j]],
                colspan = element["colspan"],
                rowspan = element["rowspan"];
                column += colspan;
                table_cell.colSpan = colspan;
                table_cell.rowSpan = rowspan;
                table_cell.innerText = element["value"] || "";
                table_cell.className = "excel-table-body-cell";
                table_row.appendChild(table_cell);
            }
            for (let j = column; j < table_width; j++) {
                let table_cell = document.createElement("td");
                table_cell.className = "excel-table-body-cell";
                table_row.appendChild(table_cell);
            }
            table_body.appendChild(table_row);
        }
        return table;
    } catch (error) {
        console.log(error);
    }
}
function Table(tbl)
    local simpleTable = pandoc.utils.to_simple_table(tbl)
    local blocks = pandoc.Blocks{}
  
    local function create_latex_row(cells)
      local latex_row = ""
      for i, cell in ipairs(cells) do
        for _, content in ipairs(cell) do
          latex_row = latex_row .. pandoc.write(pandoc.Pandoc({content}), "latex")
        end
        if i < #cells then
          latex_row = latex_row .. " & "
        end
      end
      return latex_row .. " \\\\"
    end
  
    local num_cols = 0
    if simpleTable.header and #simpleTable.header > 0 then
      num_cols = #simpleTable.header
    elseif #simpleTable.rows > 0 then
      num_cols = #simpleTable.rows[1]
    end
  
    local col_alignment = string.rep("l", num_cols)
  
    -- Use table* for two-column documents to span both columns
    blocks:insert(pandoc.RawBlock("latex", "\\begin{table*}[t]"))
    blocks:insert(pandoc.RawBlock("latex", "\\centering"))
  
    if tbl.caption then
      local caption_text = pandoc.utils.stringify(tbl.caption)
      blocks:insert(pandoc.RawBlock("latex", "\\caption{" .. caption_text .. "}"))
    end
  
    blocks:insert(pandoc.RawBlock("latex", "\\begin{tabular}{" .. col_alignment .. "}"))
    blocks:insert(pandoc.RawBlock("latex", "\\hline"))
  
    if simpleTable.header and #simpleTable.header > 0 then
      local header_row = create_latex_row(simpleTable.header)
      blocks:insert(pandoc.RawBlock("latex", header_row))
      blocks:insert(pandoc.RawBlock("latex", "\\hline"))
    end
  
    for _, row in ipairs(simpleTable.rows) do
      local latex_row = create_latex_row(row)
      blocks:insert(pandoc.RawBlock("latex", latex_row))
    end
  
    blocks:insert(pandoc.RawBlock("latex", "\\hline"))
    blocks:insert(pandoc.RawBlock("latex", "\\end{tabular}"))
    blocks:insert(pandoc.RawBlock("latex", "\\end{table*}"))
  
    return blocks
  end
  
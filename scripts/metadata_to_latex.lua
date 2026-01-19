function Meta(m)
  -- Ensure include-before exists and is a list
  if not m['include-before'] then
    m['include-before'] = pandoc.MetaList({})
  elseif m['include-before'].t ~= 'MetaList' then
    -- If it's a single item, wrap it in a list
    m['include-before'] = pandoc.MetaList({m['include-before']})
  end

  local headers = m['include-before']
  
  local function add_macro(name, val)
    if val then
      -- Convert the value to a string
      local val_str = pandoc.utils.stringify(val)
      -- Escape special LaTeX characters for footer display
      val_str = val_str:gsub('_', '\\_')
      -- Create a raw LaTeX block
      -- Use \def instead of \renewcommand to ensure it works whether the macro
      -- is already defined (by header.tex) or not.
      local latex_cmd = '\\def\\' .. name .. '{' .. val_str .. '}'
      table.insert(headers, pandoc.RawBlock('latex', latex_cmd))
    end
  end
  
  add_macro('docid', m.docID)
  add_macro('docversion', m.version)
  add_macro('docdate', m.date)
  add_macro('docauthor', m.author)
  
  -- Extract pdf_metadata for external processing
  -- This stores the metadata in a special variable that the shell script can read
  if m['pdf_metadata'] then
    local pdf_meta = m['pdf_metadata']
    
    -- Create JSON representation of pdf_metadata
    -- Store as raw LaTeX comment so it doesn't appear in PDF but can be extracted
    local json_parts = {}
    
    if pdf_meta['title'] then
      table.insert(json_parts, '"title":"' .. pandoc.utils.stringify(pdf_meta['title']):gsub('"', '\\"') .. '"')
    end
    if pdf_meta['subject'] then
      table.insert(json_parts, '"subject":"' .. pandoc.utils.stringify(pdf_meta['subject']):gsub('"', '\\"') .. '"')
    end
    if pdf_meta['keywords'] then
      table.insert(json_parts, '"keywords":"' .. pandoc.utils.stringify(pdf_meta['keywords']):gsub('"', '\\"') .. '"')
    end
    if pdf_meta['creator'] then
      table.insert(json_parts, '"creator":"' .. pandoc.utils.stringify(pdf_meta['creator']):gsub('"', '\\"') .. '"')
    end
    
    if #json_parts > 0 then
      local json_str = '{' .. table.concat(json_parts, ',') .. '}'
      -- Store as a macro that contains the JSON (for shell extraction)
      local latex_cmd = '\\def\\pdfmetadatajson{' .. json_str .. '}'
      table.insert(headers, pandoc.RawBlock('latex', latex_cmd))
    end
  end
  
  m['include-before'] = headers
  return m
end

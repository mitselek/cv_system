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
  
  m['include-before'] = headers
  return m
end

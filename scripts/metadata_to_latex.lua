function Meta(m)
  -- Ensure header-includes exists and is a list
  if not m['header-includes'] then
    m['header-includes'] = pandoc.MetaList({})
  elseif m['header-includes'].t ~= 'MetaList' then
    -- If it's a single item, wrap it in a list
    m['header-includes'] = pandoc.MetaList({m['header-includes']})
  end

  local headers = m['header-includes']
  
  local function add_macro(name, val)
    if val then
      -- Convert the value to a string
      local val_str = pandoc.utils.stringify(val)
      -- Create a raw LaTeX block
      local latex_cmd = '\\renewcommand{\\' .. name .. '}{' .. val_str .. '}'
      table.insert(headers, pandoc.RawBlock('tex', latex_cmd))
    end
  end
  
  add_macro('docid', m.docID)
  add_macro('docversion', m.version)
  add_macro('docdate', m.date)
  add_macro('docauthor', m.author)
  
  m['header-includes'] = headers
  return m
end

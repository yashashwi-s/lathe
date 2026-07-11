function Math(el)
  -- Escape backticks just in case the math contains them
  local text = string.gsub(el.text, "`", "\\`")
  if el.mathtype == 'InlineMath' then
    local mitex_code = '#mi(`' .. text .. '`)'
    return pandoc.RawInline('typst', mitex_code)
  else
    local mitex_code = '#mitex(`' .. text .. '`)'
    -- Use Typst math block for DisplayMath so it gets centered and spaced properly
    return pandoc.RawInline('typst', '$ #mitex(`' .. text .. '`) $')
  end
end

-- Also let's try to pass raw latex blocks untouched so mitex could theoretically handle them, 
-- but pandoc usually parses environments. We will just focus on Math for this naive approx.

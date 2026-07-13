function Math(el)
  local text = string.gsub(el.text, "`", "\\`")
  text = string.gsub(text, "\\label%s*{%s*[^}]+%s*}", "")
  text = string.gsub(text, "\\begin%s*{%s*equation%*?%s*}", "")
  text = string.gsub(text, "\\end%s*{%s*equation%*?%s*}", "")
  text = string.gsub(text, "\\begin%s*{%s*align%*?%s*}", "\\begin{aligned}")
  text = string.gsub(text, "\\end%s*{%s*align%*?%s*}", "\\end{aligned}")
  text = string.gsub(text, "\\d%s", "\\mathrm{d} ")
  text = string.gsub(text, "\\d([A-Za-z])", "\\mathrm{d} %1")
  text = string.gsub(text, "\\slash", "/")
  if el.mathtype == 'InlineMath' then
    return pandoc.RawInline('typst', '#mi(`' .. text .. '`)')
  end
  return pandoc.RawInline('typst', '$ #mitex(`' .. text .. '`) $')
end

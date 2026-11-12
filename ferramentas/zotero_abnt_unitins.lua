local items_path = os.getenv('UNITINS_ZOTERO_ITEMS')
if not items_path then
  error('UNITINS_ZOTERO_ITEMS nao foi definido.')
end

local file, open_error = io.open(items_path, 'rb')
if not file then
  error('Nao foi possivel abrir os metadados do Zotero: ' .. tostring(open_error))
end
local items = pandoc.json.decode(file:read('*all'))
file:close()

local items_by_key = {}
for _, item in ipairs(items) do
  items_by_key[item.id] = item
end

local function xml_escape(value)
  return tostring(value)
    :gsub('&', '&amp;')
    :gsub('<', '&lt;')
    :gsub('>', '&gt;')
    :gsub('"', '&quot;')
    :gsub("'", '&apos;')
end

local next_id = 1000

function Pandoc(document)
  document = pandoc.utils.citeproc(document)
  return document:walk({
    Cite = function(cite)
      local content = cite.content:walk({
        SmallCaps = function(element)
          return pandoc.Str(pandoc.text.upper(pandoc.utils.stringify(element)))
        end
      })
      local visible_text = pandoc.utils.stringify(content)
      local author_prefix = ''
      if #cite.citations == 1 and cite.citations[1].mode == 'AuthorInText' then
        local author, year = visible_text:match('^(.-)%s+(%b())$')
        if not author or not year then
          error('Nao foi possivel separar o autor e o ano: ' .. visible_text)
        end
        author_prefix = '<w:r><w:t xml:space="preserve">'
          .. xml_escape(author .. ' ') .. '</w:t></w:r>'
        visible_text = year
      end

      local citation_items = {}
      for _, citation in ipairs(cite.citations) do
        local item = items_by_key[citation.id]
        if not item or not item.custom or not item.custom.itemID or not item.custom.uri then
          error('Faltam metadados do Zotero para a citacao: ' .. citation.id)
        end
        local item_data = {}
        for key, value in pairs(item) do
          if key ~= 'custom' then
            item_data[key] = value
          end
        end
        local entry = {
          id = item.custom.itemID,
          uris = { item.custom.uri },
          itemData = item_data
        }
        if citation.mode == 'AuthorInText' or citation.mode == 'SuppressAuthor' then
          entry['suppress-author'] = true
        end
        table.insert(citation_items, entry)
      end

      next_id = next_id + 1
      local payload = {
        citationID = 'zot' .. tostring(next_id),
        properties = {
          formattedCitation = visible_text,
          plainCitation = visible_text,
          noteIndex = 0
        },
        citationItems = citation_items,
        schema = 'https://github.com/citation-style-language/schema/raw/master/csl-citation.json'
      }
      local instruction = ' ADDIN ZOTERO_ITEM CSL_CITATION '
        .. xml_escape(pandoc.json.encode(payload)) .. ' '
      local field = author_prefix .. '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        .. '<w:r><w:instrText xml:space="preserve">' .. instruction .. '</w:instrText></w:r>'
        .. '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        .. '<w:r><w:rPr><w:noProof/></w:rPr><w:t xml:space="preserve">'
        .. xml_escape(visible_text) .. '</w:t></w:r>'
        .. '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
      return pandoc.RawInline('openxml', field)
    end
  })
end

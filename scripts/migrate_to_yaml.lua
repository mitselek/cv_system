#!/usr/bin/env lua

-- =============================================================================
-- MIGRATION SCRIPT: HTML Comments -> YAML Frontmatter
-- =============================================================================
--
-- This script demonstrates the basics of Lua programming:
-- 1. File I/O (Input/Output)
-- 2. String Pattern Matching (Lua's alternative to Regex)
-- 3. Tables (Lua's universal data structure)
-- 4. System calls (interacting with the shell)
--
-- Usage: lua scripts/migrate_to_yaml.lua
-- =============================================================================

-- In Lua, variables are global by default.
-- Always use 'local' unless you specifically want a global variable.
local lfs_command = "find applications -name '*.md'"

-- -----------------------------------------------------------------------------
-- Helper Function: Read the entire content of a file
-- -----------------------------------------------------------------------------
local function read_file(path)
    -- io.open returns a file handle or nil + error message
    local file, err = io.open(path, "r")
    if not file then
        print("Error opening file: " .. err)
        return nil
    end

    -- '*a' reads the whole file at once
    local content = file:read("*a")
    file:close()
    return content
end

-- -----------------------------------------------------------------------------
-- Helper Function: Write content back to a file
-- -----------------------------------------------------------------------------
local function write_file(path, content)
    local file, err = io.open(path, "w")
    if not file then
        print("Error writing file: " .. err)
        return false
    end
    file:write(content)
    file:close()
    return true
end

-- -----------------------------------------------------------------------------
-- Core Logic: Parse HTML metadata and convert to YAML
-- -----------------------------------------------------------------------------
local function convert_content(content)
    -- Lua Patterns vs Regex:
    -- .  = any character
    -- -  = 0 or more repetitions (lazy/non-greedy) - equivalent to *? in regex
    -- %s = whitespace
    -- () = capture group

    -- 1. Find the HTML comment block at the start of the file
    -- We look for <!-- followed by anything (lazy) until -->
    local comment_pattern = "^%s*<!%-%-(.-)%-%->"
    
    -- string.match returns the captured group (the content inside the comment)
    local metadata_block = content:match(comment_pattern)

    if not metadata_block then
        return nil, "No HTML metadata found"
    end

    -- 2. Check if it contains our target fields (docID)
    if not metadata_block:find("docID:") then
        return nil, "HTML comment found, but no docID present"
    end

    -- 3. Extract fields using patterns
    -- %w+  = one or more alphanumeric characters (word)
    -- :    = literal colon
    -- %s*  = zero or more whitespace
    -- (.-) = capture everything non-greedily...
    -- $    = ...until the end of the string (or newline in iteration)
    
    -- We'll use a Lua table (dictionary) to store results
    local meta = {}
    
    -- Helper to extract a specific key
    -- We look for "key:", optional space, capture content, then a newline or end of string
    local function extract(key)
        -- Pattern explanation:
        -- key .. ":"  -> concatenates string, e.g., "docID:"
        -- %s*         -> matches optional spaces
        -- ([^%s]+)    -> captures non-whitespace characters (simple word)
        -- OR for author we need to capture until end of line or specific delimiter
        
        -- Let's try a more robust approach: iterating over key-value pairs isn't easy 
        -- because the format wasn't strict JSON/YAML. It was loose text.
        
        -- Specific pattern for our known format: "key: value"
        -- We assume values don't contain newlines for now.
        local val = metadata_block:match(key .. ":%s*([^\n\r]+)")
        
        -- Clean up trailing spaces or other attributes if they were on one line
        if val then
            -- If the line continues with another key (e.g. "version: 1.0 date: ...")
            -- we need to stop at the next key.
            -- This is tricky in Lua patterns without lookaheads.
            -- Strategy: Split by known keys?
            
            -- Simpler strategy for this specific legacy format:
            -- The legacy format often had multiple keys on one line or separate lines.
            -- Let's try to capture "key: value" where value ends at a space followed by a known key OR end of string.
            
            -- Actually, let's just grab the specific values we know exist.
            return val
        end
    end

    -- Let's refine extraction. The legacy format was often:
    -- docID: ... version: ... date: ... author: ...
    -- All on one line or multiple.
    
    -- We can iterate over the string looking for "key: value"
    -- But since we know the keys, let's find them specifically.
    
    -- We need to handle the case where multiple keys are on one line.
    -- Example: "docID: A version: 1"
    -- Pattern for docID: "docID:%s*([^%s]+)" -> captures until next space
    
    meta.docID = metadata_block:match("docID:%s*([^%s]+)")
    meta.version = metadata_block:match("version:%s*([^%s]+)")
    meta.date = metadata_block:match("date:%s*([^%s]+)")
    
    -- Author is tricky because it might have spaces "Michele K"
    -- It is usually the last item.
    -- Let's try to capture "author:" until the end of the comment string
    -- We use [^>]+ to capture everything until the closing tag of the comment might appear
    -- or just until the end of the captured block.
    meta.author = metadata_block:match("author:%s*(.+)")
    
    -- Clean up author: remove trailing spaces or newlines
    if meta.author then
        meta.author = meta.author:gsub("^%s*(.-)%s*$", "%1")
    end

    if not meta.docID then return nil, "Could not parse docID" end

    -- 4. Construct YAML Frontmatter
    -- .. is the string concatenation operator
    local yaml = "---\n" ..
                 "docID: " .. (meta.docID or "") .. "\n" ..
                 "version: " .. (meta.version or "") .. "\n" ..
                 "date: " .. (meta.date or "") .. "\n" ..
                 "author: " .. (meta.author or "Unknown") .. "\n" ..
                 "---\n"

    -- 5. Replace the HTML comment with YAML
    -- We escape the pattern magic characters in the original block to replace it literally
    -- Actually, string.gsub can take a pattern.
    
    -- Easier way: We know where the file started.
    -- We remove the match and prepend YAML.
    
    -- Remove the first occurrence of the comment pattern
    local new_content = content:gsub(comment_pattern, "", 1)
    
    -- Trim leading whitespace that might be left over
    new_content = new_content:gsub("^%s+", "")
    
    return yaml .. "\n" .. new_content
end

-- -----------------------------------------------------------------------------
-- Main Execution Loop
-- -----------------------------------------------------------------------------
print("Starting migration to YAML frontmatter...")

-- io.popen executes a shell command and lets us read the output
local handle = io.popen(lfs_command)
local result = handle:read("*a")
handle:close()

-- Iterate over lines (filenames)
for filename in result:gmatch("[^\r\n]+") do
    local content = read_file(filename)
    if content then
        local new_content, msg = convert_content(content)
        
        if new_content then
            write_file(filename, new_content)
            print("[OK] Migrated: " .. filename)
        else
            -- If msg is nil, it means it just didn't match (not an error, maybe already migrated)
            if msg and msg ~= "No HTML metadata found" then
                print("[SKIP] " .. filename .. ": " .. msg)
            end
        end
    end
end

print("Migration complete.")

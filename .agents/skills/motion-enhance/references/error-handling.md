# Error Handling — motion-enhance

Structured guide for handling edge cases and failures in the motion-enhance workflow.

## File Reading Errors

### File Not Found
**Symptom:** `Read` tool returns file doesn't exist
**Trigger:** Invalid path, wrong extension, file was deleted
**Recovery:**
1. Confirm the path with the user: "I couldn't find `file.html` at the path you provided. Can you verify the exact path?"
2. Ask if the file has a different name or location
3. If the user provides a new path, retry the read

### File Too Large (>5MB)
**Symptom:** `Read` tool fails or returns truncated content
**Trigger:** File exceeds processing limits
**Recovery:**
1. Split the file by sections: "This file is too large to process all at once. Let me analyze the HTML structure first, then CSS, then JavaScript separately."
2. Process in chunks (HTML → CSS → JS/GSAP)
3. Create separate audit reports per section if needed

### Encoding Issues
**Symptom:** File contains invalid UTF-8 or mixed encodings
**Trigger:** File was edited in non-UTF8 editor, has binary content mixed in
**Recovery:**
1. Ask the user to save the file as UTF-8
2. If possible, extract just the animation code sections manually
3. Proceed with what's readable

### File is Not HTML/CSS/JS
**Symptom:** File extension claims to be `.html` but content is binary or wrong format
**Trigger:** Wrong file uploaded, file renamed incorrectly
**Recovery:**
1. Identify the actual file type from content
2. Explain: "This file appears to be [TYPE], not HTML. I can only audit web animation code."
3. Ask the user to upload the correct file

## Site Type Detection Errors

### Site Type Can't Be Determined
**Symptom:** HTML structure doesn't match any known site type (marketing-landing, portfolio, saas-app, docs-blog, e-commerce)
**Trigger:** Custom or hybrid site structure
**Recovery:**
1. Default to `site_type: "unknown"`
2. Load baseline patterns for "unknown": focus on CRITICAL/WARNING issues only, skip pattern recommendations
3. Inform the user: "I couldn't classify your site, so I'm focusing on universal animation best practices. Your site type is: unknown"
4. Offer to clarify if the user specifies: "Is this a [option A], [option B], or something else?"

### Multiple Possible Site Types
**Symptom:** Site matches multiple classifications (e.g., both "portfolio" and "saas-app" characteristics)
**Trigger:** Hybrid or complex architecture
**Recovery:**
1. Ask the user: "Is this primarily a [site type 1] or [site type 2]?"
2. Use the user's answer as the authoritative site_type
3. If user is unsure, pick the one that applies to the animation sections they care about

## Pattern Application Errors

### Pattern Can't Be Applied
**Symptom:** A detected pattern (scroll-trigger-reveal, morphing-button-states, etc.) fails to apply
**Trigger:** Code structure doesn't match pattern prerequisites, missing HTML elements, conflicting code
**Recovery:**
1. Skip the pattern and note it as SKIPPED in the summary
2. Document the reason: `SKIPPED: scroll-trigger-reveal — no scroll-based animations detected`
3. Continue with other applicable patterns
4. Don't force-apply a pattern if prerequisites aren't met

### Missing Required Elements for Pattern
**Symptom:** Pattern requires specific HTML structure or CSS classes that don't exist
**Trigger:** User asked to apply pattern to code that isn't compatible
**Recovery:**
1. Suggest the structural change needed: "To use the [pattern name] pattern, you'd need to add [required structure]"
2. Offer the user two options:
   - Option A: Restructure the HTML and apply the pattern
   - Option B: Skip this pattern and focus on other improvements
3. Don't apply the pattern unless the user explicitly agrees to restructure

### Conflicting Code Already Present
**Symptom:** The fix would conflict with or overwrite existing code
**Trigger:** User has existing animation code that's incompatible with the pattern
**Recovery:**
1. Identify the conflict: "Your code has [existing animation] that would conflict with [proposed fix]"
2. Ask the user: "Should I replace this with the new pattern, or keep your existing code?"
3. Only apply fixes if the user explicitly approves

## Audit/Fix Execution Errors

### Edit Tool Fails
**Symptom:** `Edit` tool returns error when trying to apply fixes
**Trigger:** Syntax error in replacement string, conflicting edits, file permissions
**Recovery:**
1. Review the replacement string for syntax errors
2. If it's a malformed string, rebuild it more carefully
3. If it's a permission issue, ask the user: "I don't have permission to edit this file. Can you check file permissions or try saving it first?"
4. Offer to provide the fixes as a separate file instead

### CRITICAL Issue Can't Be Fixed
**Symptom:** A CRITICAL audit finding can't be fixed automatically
**Trigger:** Complex refactoring needed, user's code structure is unusual
**Recovery:**
1. Provide a detailed manual fix: "Here's the code change you need to make manually: [code]"
2. Explain why: "This requires restructuring your animation timeline, which I can't do automatically because [reason]"
3. Mark as MANUAL in the summary: `CRITICAL: CDN 404 on SplitText — MANUAL FIX REQUIRED`

### Parallel Agent Fails
**Symptom:** One of multiple agents processing files returns an error
**Trigger:** File is corrupted, agent runs out of tokens, agent encounters unexpected syntax
**Recovery:**
1. **For that specific file:** Mark as ERROR in the summary, explain what went wrong
2. **Continue with other files:** Don't halt all processing
3. **Offer retry:** "File [name] failed to process. Would you like me to try again?"
4. **Provide partial results:** Return fixes for successfully processed files, note failures

## Output & Verification Errors

### Summary Table Has Errors
**Symptom:** Severity table shows inconsistent data (e.g., APPLIED patterns that weren't actually in the file)
**Trigger:** Mismatch between audit findings and applied fixes
**Recovery:**
1. Re-verify the file contents against the table
2. Correct the table to match actual fixes: "I made an error in the summary. Here's the corrected table:"
3. Show the diff between what was claimed and what was actually done

### Visual Verification Needed But Can't Be Performed
**Symptom:** User wants to see the enhanced file rendered, but we can't generate screenshots
**Trigger:** No screenshot capability in current environment
**Recovery:**
1. Explain: "I've applied the fixes to your code, but I can't render a screenshot in this environment."
2. Offer alternatives:
   - Option A: Provide the enhanced file; user can preview locally
   - Option B: Provide a summary of changes and invite user to verify
3. Include a checklist: "After applying these fixes, test for: [list of things to verify]"

### Syntax Validation Fails
**Symptom:** Enhanced file has syntax errors after fixes
**Trigger:** Invalid JavaScript/CSS/HTML generated or introduced
**Recovery:**
1. Identify the error: "I introduced a syntax error at line [N]: [error description]"
2. Fix it immediately: Reapply the edit with corrected syntax
3. Re-validate
4. If still broken, provide the raw code and ask the user to validate: "Here's the problematic code. Can you help identify the error?"

## User Communication Errors

### User Doesn't Understand the Fix
**Symptom:** User asks "Why did you change X to Y?" or the fix seems wrong to them
**Trigger:** Explanation was too technical, user expected something different
**Recovery:**
1. Explain in simpler terms: "This change prevents [jank/conflict/performance issue] by [plain English explanation]"
2. Provide context: "The audit flagged this as a CRITICAL issue because [reason]"
3. Offer to revert: "If you prefer the original code, I can undo this change"

### User Rejects the Enhanced File
**Symptom:** User says "I don't want these changes"
**Trigger:** User disagrees with the audit findings or fixes
**Recovery:**
1. Ask why: "Which changes do you want to keep or remove?"
2. Provide selective fixes: "I can apply fixes A and C, but leave B unchanged"
3. If user rejects all fixes, don't force them: "I'll keep your original file and provide the audit findings for you to review"

## Fallback Strategies

### When in Doubt, Provide Audit Only
If the fix is uncertain, risky, or complex:
1. Skip the auto-fix
2. Return the audit severity table with manual recommendations
3. Let the user decide whether to apply changes

### When Multiple Approaches Exist
If there are multiple valid ways to fix an issue:
1. Note this in the output: "This CRITICAL issue can be fixed 3 ways. Here's the recommended approach: [approach 1]. Alternatives: [2], [3]"
2. Apply the recommended one automatically
3. Offer the alternatives as reference

### When Uncertain About Site Type
Default to conservative approach:
1. Use `site_type: "unknown"`
2. Apply only CRITICAL and WARNING fixes
3. Skip INFO items and pattern recommendations
4. Explain to user: "I applied critical fixes conservatively because I couldn't determine your site type"

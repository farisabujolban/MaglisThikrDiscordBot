Good Figma Design Principles:

1. Any frame used more than once should be a compnent
2. Any text style used more than once should be a text style
3. Any frame should have an auto layout
4. Any frame should have two or more items if only one ungroup it
5. An insatance it just a copy of the compnent any change to it wouldn't affect it's use
6. Try resizing a frame. If children reflow correctly and nothing overlaps or disappears, you're constrained. If things break or float, you're not
7. Spacing uses a consistent scale (8px grid(letter size))
8. Any color used more than once should be a color style
9. Any core UI element (button, card, input, nav bar) should be a component

AI workflow tips:

1. Make EPICS, user stories, and tasks for a spec driven architecture
2. Let 2 seperate agents work one for making test cases and one for writing the code for test driven architecture to work well with the spec driven architecture to get the best of both worlds
3. Use Gemini for the test cases and Claude for writing code

things to add to codeanchor:

1. check if the npm packages being downloaded are safe and that they exist(slop squatting) and lock the version in package-lock.json
2. check for rate limiting middleware
3. check for row level security(RLS) being on in supabasue
4. check for insecure direct object reference(url based id routing because urls are changable some user can access other user's data by modifying the url in seconds)
5. check for mass assignment(sending more data than needed in a request sometimes senstive data)
6. check for race conditions by checking how the tables are made when a user clicks something require processing it should be set to unique by user id to handle multiple clicks, also suggest that the ui shows that button has been clicked by showing some type of visual like the utton greying out and a pop up saying processing
7. check hardcoded urls so when deployed the app is not pointing to localhost, environment variables for api url should do it

things I learned:

1. storage objects are used to store images and audios for users
2. use rem instead of px
3. use hsl instead of rgb
4. websites gain more attraction the more authority they have and they can gain it by being linked by other trusted websites
5. every page should have an error, loading, and success states
6. always use serverless unless you are building something that require the server to be running most of the time because the startup time for serverless take time
7. use dafety features for agents like blocked commands, read-only mode, and hooks
8. I don't like the word AI when describing a product it eliminates its purpose use this format instead:
   Quarry helps [specfic userbase e.g. job seekers] achieve [spefic outcome e.g. applying for jobs] without [painful current process e.g. time it takes to fill up job applications when the info itself is repetitive]
9. Row Level Security (RLS) Audits (0:48 - 6:26):

Verify Policy Logic: Ensure RLS policies are not just technically present but logically sound. Ask the AI: "Can a user access, modify, or delete data belonging to another user?"
Sensitive Data Isolation: Ensure critical fields like subscription_status, user_role, or rate_limits are not stored in the same table as user-editable data. If they are, they must be protected by more restrictive, non-bypassable policies.
Exhaustive Testing: Explicitly prompt the AI to find scenarios where a user could manipulate their own permissions (e.g., granting themselves premium access). 10. Rate Limiting Implementation (7:31 - 9:52):

Backend-Side Enforcement: Do not rely on frontend checks. Ensure rate limits are implemented at the backend/API level.
User-Based Rate Limits: Ensure there is a mechanism to track request counts per user and block them if they exceed limits.
IP-Based Rate Limiting: Implement secondary protection to block or throttle suspicious traffic based on IP address to prevent mass-account abuse. 11. Sensitive API Calls (9:52 - 11:49):

No Frontend API Secrets: Ensure no sensitive keys (e.g., Stripe, SendGrid, AWS) are called directly from the frontend or exposed in environment variables visible to the client.
Backend-Only Proxies: All sensitive calls must be routed through your own backend or serverless functions (Supabase / Firebase functions). 12. Financial & Budget Controls (11:49 - 13:09):

Budget Caps: Verify that your cloud provider has a hard budget cap that shuts down services if a threshold is hit.
Usage Alerts: If a hard cap isn't available, ensure automated alerts are configured to notify you immediately if spending spikes. 13. Proactive Security (13:09 - 15:08):

Use MCPs: Integrate the Supabase or Firebase MCPs (Model Context Protocol) into your IDE so the AI has direct access to your infrastructure configuration for a more accurate audit.
Adversarial Prompting: Ask the AI to "Think like a pentester" and attempt to break your application logic, specifically targeting billing, data privacy, and authentication workflows.

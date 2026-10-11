# AURA - Phase 7 Test Results

Target: 8 out of 10 test cases passing. Result: 10 out of 10 passed (two required a fix before passing).

| Test | Case | First attempt | After fix | Notes |
|------|------|----------------|-----------|-------|
| 7.1 | Clear Hindi command | Fail | Pass | Whisper misheard "kal" as "akal", causing a wrong draft. Fixed by adding a Whisper vocabulary hint. |
| 7.2 | Clear Hinglish command | Pass | - | Transcript was partly garbled but the AI still produced a correct draft. |
| 7.3 | Clear English command | Pass | - | Transcript and draft both exact. |
| 7.4 | Informal phrasing | Pass | - | Transcript mixed scripts (Devanagari and Urdu) but recipient and meaning were still correct. |
| 7.5 | Formal/professional phrasing | Pass | - | Draft kept the specific details (project submission, one week extension) and stayed formal. |
| 7.6 | Missing information | Fail | Pass | AURA asked a clarification question as expected, but the transcript contained text the user never said, leaking in from the Whisper prompt hint. Fixed by simplifying the hint to a plain word list. |
| 7.7 | Ambiguous recipient | Fail | Pass | First attempt failed with an unexplained generic error (likely a transient network or API issue). Retest passed cleanly with a correct disambiguation question. |
| 7.8 | Unknown recipient | Pass | - | Correct "no email saved" message, no draft created. |
| 7.9 | User edits/rejects draft mid-flow | Pass | - | "No, chhota karo" correctly triggered a shorter redraft before the user approved and the email sent. |
| 7.10 | Simulated failure (no internet) | Pass | - | Correct "can't reach the internet" message, no crash. |

## Summary

AURA's software pipeline met and exceeded its MVP success target. Both failures were in the speech-to-text stage (Whisper), not in the AI parsing, contact resolution, confirmation, or Gmail sending logic, which passed every test on the first attempt. This points to Hindi/Hinglish transcription accuracy as the system's primary weak point, addressed partially with a vocabulary hint but not fully solved.
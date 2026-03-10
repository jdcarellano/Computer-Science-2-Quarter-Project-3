# Changelog

All notable changes to the Website Checker project will be documented in this file.

---

## 2026-03-09
### Added
- Added interactive CLI menu system for managing websites.
- Added option to view a specific website by ID.
- Added confirmation prompt before deleting a website.

### Improved
- Improved input validation for menu selections and IDs.
- Improved output formatting when displaying websites.

---

## 2026-03-08
### Added
- Added `display_all()` function to show all stored websites.
- Added `read_website()` to retrieve a single website record.

### Changed
- Modified database query to include the `reason` field in outputs.

---

## 2026-03-07
### Added
- Implemented `check_all()` function to automatically check all websites in the database.
- Integrated status and safety checks into a single automated workflow.

---

## 2026-03-06
### Added
- Implemented `check_status(url)` function to detect if a website is up or down.
- Added timeout handling for URL requests.

### Fixed
- Handled connection errors when checking unreachable websites.

---

## 2026-03-05
### Added
- Implemented `check_safety(url)` function to perform a basic HTTPS safety check.
- Added reason messages explaining safety status.

---

## 2026-03-04
### Added
- Added `update_reason()` function to modify the safety explanation for a website.

### Changed
- Extended the database schema to include a `reason` column.

---

## 2026-03-03
### Added
- Added `update_safety()` function to update a website’s safety status.
- Added optional reason parameter when updating safety.

---

## 2026-03-02
### Added
- Implemented `update_status()` function to update the website status.
- Added automatic timestamp for `last_checked`.

---

## 2026-03-01
### Added
- Implemented `delete_website()` function for removing websites from the database.

---

## 2026-02-28
### Added
- Implemented `read_websites()` function to retrieve all websites from the database.

---

## 2026-02-27
### Added
- Implemented `create_website()` function to insert new website records.

---

## 2026-02-20
### Added
- Added SQLite database integration using `sqlite3`.
- Created `websites` table structure with fields:
  - id
  - url
  - status
  - safety
  - last_checked

---

## 2026-02-14
### Initial Commit
### Added
- Created the initial project structure.
- Implemented database initialization with `init_db()`.
- Set up automatic database and table creation if not existing.

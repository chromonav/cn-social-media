# Product Requirements Document: Automated Commit Collection & Analysis System

## Document Information
- **Version**: 1.0
- **Purpose**: Define requirements for an automated system that collects, analyzes, and maps Git commits to employees for social media content generation
- **Target Module**: Social Media Management
- **Frappe App**: cn_social_media

## Executive Summary

The Automated Commit Collection & Analysis System transforms development activities into compelling social media content by systematically collecting Git commits, classifying them by type and business impact, mapping them to employees, and generating a Development Activity Log that feeds the content creation pipeline.

This system addresses the critical gap between technical development work and marketing-ready content by providing automated discovery, classification, and scoring of code contributions that demonstrate business value to target audiences (CIOs, CTOs, CFOs, Plant Managers, HR Directors).

**Key Benefits**:
- Automated discovery of content-worthy development activities
- Systematic classification and business impact scoring
- Employee attribution and bot filtering
- Seamless integration with existing social media content pipeline
- Reduction of manual content discovery effort by 80%

## System Architecture

```
┌─────────────────────── Git Repositories ──────────────────────┐
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Repository 1 │  │ Repository 2 │  │ Repository N │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
└─────────┼─────────────────┼─────────────────┼────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
┌─────────────────── Collection Engine ─────────────────────────┐
│                           ▼                                    │
│  ┌──────────────────────────────────────┐                    │
│  │       Commit Collector                │◄───┐               │
│  └──────────────┬───────────────────────┘    │               │
│                 │                              │               │
│  ┌──────────────┴──────────┐  ┌──────────────┴──────────┐   │
│  │   Timestamp Manager      │  │   Repository Scanner     │   │
│  └──────────────────────────┘  └─────────────────────────┘   │
└────────────────────────────┬──────────────────────────────────┘
                             │
┌──────────────────── Processing Pipeline ──────────────────────┐
│                           ▼                                    │
│  ┌──────────────────────────────────────┐                    │
│  │       Commit Classifier               │                    │
│  └──────────────┬───────────────────────┘                    │
│                 ▼                                              │
│  ┌──────────────────────────────────────┐                    │
│  │       Employee Mapper                 │                    │
│  └──────────────┬───────────────────────┘                    │
│                 ▼                                              │
│  ┌──────────────────────────────────────┐                    │
│  │       Bot Filter                      │                    │
│  └──────────────┬───────────────────────┘                    │
│                 ▼                                              │
│  ┌──────────────────────────────────────┐                    │
│  │       Impact Scorer                   │                    │
│  └──────────────┬───────────────────────┘                    │
└─────────────────┼──────────────────────────────────────────────┘
                  │
┌─────────────────────── Storage Layer ─────────────────────────┐
│                 ▼                                              │
│  ┌──────────────────────────────────────┐                    │
│  │ 🗄️  Development Activity Log         │◄───────┐           │
│  └──────────────┬───────────────────────┘        │           │
│                 │                                  │           │
│  ┌──────────────┴──────────┐  ┌──────────────────┴────────┐ │
│  │ 🗄️  Employee Records    │  │ 🗄️  Classification Rules │ │
│  └──────────────────────────┘  └───────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────┐                    │
│  │ 🗄️  Business Impact Matrix          │────────────┐       │
│  └──────────────────────────────────────┘            │       │
└───────────────────┬────────────────────────────────────┼───────┘
                    │                                    │
┌─────────── Integration Layer ──────────────────────────┼───────┐
│                   ▼                                    │       │
│  ┌──────────────────────────────────────┐             │       │
│  │  Content Opportunity Detector         │◄────────────┘       │
│  └──────────────┬───────────────────────┘                     │
│                 ▼                                              │
│  ┌──────────────────────────────────────┐                    │
│  │  Social Media Pipeline API            │                    │
│  └──────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘

Legend: 🗄️ = Database/Storage Component
```

## Core Components

### DocTypes
| DocType | Type | Purpose | Key Fields |
|---------|------|---------|------------|
| Development Activity Log | Transaction | Track processed commits with business impact | commit_hash, author, timestamp, classification, impact_score |
| Commit Collection Run | Transaction | Track collection execution periods | start_timestamp, end_timestamp, status, commits_processed |
| Employee Mapping | Master | Map Git authors to employee records | git_email, git_name, employee_id, is_active |
| Classification Rule | Master | Define commit type classification logic | pattern, commit_type, keywords, weight |
| Business Impact Matrix | Master | Score commits by type and business value | commit_type, role_target, impact_score, content_worthy |
| Repository Configuration | Master | Configure monitored repositories | repo_path, branch, is_active, collection_frequency |

### Relationships
```
Repository Config ──1:N──> Commit Collection Run ──1:N──> Development Activity Log
Employee Mapping ──1:N──> Development Activity Log
Classification Rule ──1:N──> Development Activity Log
Business Impact Matrix ──1:N──> Development Activity Log
```

## Workflow

```
┌─────────────────── Commit Processing State Flow ───────────────────┐
│                                                                     │
│     ┌──────────┐                                                   │
│     │   Start  │                                                   │
│     └────┬─────┘                                                   │
│          │                                                         │
│          ▼                                                         │
│     ┌──────────┐      Timer           ┌──────────────┐           │
│     │Scheduled │─────Triggered───────▶│  Collecting   │           │
│     └──────────┘                      └──────┬───────┘           │
│                                              │                     │
│                                    Raw Commits│Retrieved           │
│                                              ▼                     │
│                                       ┌──────────────┐            │
│                                       │  Processing   │            │
│                                       └──────┬───────┘            │
│                                              │                     │
│                                    Filtered &│Mapped               │
│                                              ▼                     │
│                                       ┌──────────────┐            │
│                                       │ Classifying   │            │
│                                       └──────┬───────┘            │
│                                              │                     │
│                                        Types │Assigned             │
│                                              ▼                     │
│                                       ┌──────────────┐            │
│                                       │   Scoring     │            │
│                                       └──────┬───────┘            │
│                                              │                     │
│                                       Impact │Calculated           │
│                                              ▼                     │
│                                       ┌──────────────┐            │
│                                       │   Storing     │            │
│                                       └──────┬───────┘            │
│                                              │                     │
│                                  Activity Log│Updated              │
│                                              ▼                     │
│                                       ┌──────────────┐            │
│                                       │  Completed    │            │
│                                       └──────┬───────┘            │
│                                              │                     │
│                                   Auto       │Trigger              │
│                                              ▼                     │
│                             ┌─────────────────────────────┐       │
│                             │ ContentOpportunityCheck     │       │
│                             └────────────┬────────────────┘       │
│                                          │                        │
│                                High Score│Items                   │
│                                          ▼                        │
│                             ┌─────────────────────────────┐       │
│                             │   ContentGeneration         │       │
│                             └────────────┬────────────────┘       │
│                                          │                        │
│                                          ▼                        │
│                                     ┌─────────┐                   │
│                                     │   End   │                   │
│                                     └─────────┘                   │
│                                                                    │
│  ┌──────────── Error Handling Branch ────────────┐               │
│  │                                                │               │
│  │  Collecting ──Collection Error──┐             │               │
│  │  Processing ──Processing Error──┤             │               │
│  │  Classifying─Classification Error┤            │               │
│  │  Scoring ────Scoring Error──────┼──▶ Failed   │               │
│  │  Storing ────Storage Error──────┘      │      │               │
│  │                                         │      │               │
│  │                                         ▼      │               │
│  │                                   ┌─────────┐  │               │
│  │                            ┌──────│  Retry  │  │               │
│  │                            │      └────┬────┘  │               │
│  │                            │           │       │               │
│  │                     Retry  │           │Auto   │               │
│  │                     Attempt│           │Retry  │               │
│  │                            │           │(3x)   │               │
│  │                            ▼           │       │               │
│  │                       Collecting◄──────┘       │               │
│  │                                                │               │
│  │                      Max Retries               │               │
│  │                      Exceeded                  │               │
│  │                           │                    │               │
│  │                           ▼                    │               │
│  │                       ┌─────────┐              │               │
│  │                       │   End   │              │               │
│  │                       └─────────┘              │               │
│  └────────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

### Approval Matrix
| State | Role | Action |
|-------|------|--------|
| Scheduled | System | Auto-execute collection |
| Failed | Content Operations Manager | Review and retry |
| Completed | Content Operations Team | Review opportunities |
| ContentOpportunityCheck | System | Auto-identify high-impact items |

## Functional Requirements

### FR-001: Automated Commit Collection
**Description**: Collect Git commits between configurable timestamps (T0-T1) from monitored repositories.

**Acceptance Criteria**:
- System shall collect all commits between T0 and T1 timestamps
- System shall extract commit hash, author name, author email, commit message, timestamp, and files changed
- System shall handle multiple repository sources simultaneously
- System shall update T0 to current T1 after successful collection
- System shall support configurable collection frequencies (hourly, daily, weekly)
- System shall log all collection activities with success/failure status

### FR-002: Commit Classification
**Description**: Automatically classify commits by type using configurable rules and machine learning patterns.

**Acceptance Criteria**:
- System shall classify commits into categories: Feature, Bug Fix, Refactor, Documentation, Performance, Security, Configuration
- System shall use keyword matching, commit message patterns, and file path analysis
- System shall support custom classification rules via Classification Rule DocType
- System shall achieve minimum 85% classification accuracy
- System shall handle edge cases and assign "Unknown" classification when uncertain
- System shall support manual classification override

### FR-003: Employee Mapping
**Description**: Map Git commit authors to employee records using email and name matching.

**Acceptance Criteria**:
- System shall match Git author emails to employee records
- System shall handle multiple Git identities per employee
- System shall support fuzzy name matching for variations
- System shall flag unmatched authors for manual review
- System shall maintain active/inactive status for Git identities
- System shall support bulk import of Git-to-employee mappings

### FR-004: Bot and Automated Commit Filtering
**Description**: Filter out automated commits, bot commits, and merge commits that lack business value.

**Acceptance Criteria**:
- System shall identify and exclude merge commits
- System shall filter commits from known bot accounts (GitHub Actions, CI/CD systems)
- System shall exclude commits with automated patterns (version bumps, dependency updates)
- System shall support configurable bot detection rules
- System shall maintain whitelist of approved automation commits
- System shall log filtered commits for audit purposes

### FR-005: Business Impact Scoring
**Description**: Assign business impact scores to commits based on type, scope, and target audience relevance.

**Acceptance Criteria**:
- System shall assign impact scores from 1-100 based on business value
- System shall consider commit type, lines changed, and files affected
- System shall weight scores by target audience relevance (CIO, CTO, CFO, etc.)
- System shall identify content-worthy commits (score >70)
- System shall support configurable scoring matrices
- System shall provide detailed scoring breakdown and rationale

### FR-006: Development Activity Log Generation
**Description**: Generate comprehensive activity logs with all processed commit data and metadata.

**Acceptance Criteria**:
- System shall store all processed commits in Development Activity Log
- System shall include commit details, classification, employee mapping, and impact score
- System shall maintain collection run linkage for tracking
- System shall support bulk operations and data export
- System shall provide activity summaries by employee, time period, and type
- System shall maintain data integrity and audit trail

### FR-007: Content Pipeline Integration
**Description**: Integrate with existing social media content generation pipeline for automated opportunity detection.

**Acceptance Criteria**:
- System shall automatically identify high-impact commits for content creation
- System shall trigger content opportunity notifications
- System shall provide API endpoints for content pipeline integration
- System shall support real-time and batch integration modes
- System shall maintain integration status and error logging
- System shall support webhook notifications for immediate processing


## Data Models and Schema

### Development Activity Log
```json
{
  "name": "ACTLOG-2024-001",
  "commit_hash": "abc123def456",
  "repository": "frappe/erpnext",
  "branch": "main",
  "author_name": "John Developer",
  "author_email": "john@company.com",
  "employee": "EMP-001",
  "commit_message": "Add automated reconciliation feature",
  "timestamp": "2024-09-04 10:30:00",
  "files_changed": 5,
  "lines_added": 150,
  "lines_removed": 23,
  "classification": "Feature",
  "classification_confidence": 0.95,
  "business_impact_score": 85,
  "target_roles": ["CFO", "Accountant"],
  "content_worthy": 1,
  "collection_run": "RUN-2024-001",
  "created": "2024-09-04 11:00:00"
}
```

### Employee Mapping
```json
{
  "name": "EMPMAP-001",
  "employee": "EMP-001",
  "employee_name": "John Developer",
  "git_email": "john@company.com",
  "git_name": "John Developer",
  "alternative_emails": ["j.developer@company.com", "john.dev@company.com"],
  "is_active": 1,
  "created": "2024-09-04 09:00:00"
}
```

### Business Impact Matrix
```json
{
  "name": "BIM-001",
  "commit_type": "Feature",
  "target_role": "CFO",
  "base_score": 80,
  "multiplier_factors": {
    "lines_changed": 0.1,
    "files_affected": 0.05,
    "customer_facing": 1.2
  },
  "content_threshold": 70,
  "is_active": 1
}
```

## System Architecture: n8n and ERPNext Integration

### Overview
The system uses a distributed architecture where:
- **n8n**: Handles workflow orchestration, commit processing, classification, and scoring
- **ERPNext**: Provides configuration data, stores results, and manages content opportunities

n8n performs the heavy lifting of commit collection and analysis, while ERPNext serves as the configuration source and data repository.

### How the System Works

#### Component Responsibilities

**n8n Handles:**
- Scheduling and triggering collection runs
- Executing git commands to fetch commits
- Parsing and processing commit data
- Classifying commits by type
- Calculating impact scores
- Orchestrating the workflow sequence
- Sending notifications and alerts
- Retry logic and error handling

**ERPNext Handles:**
- All data storage (DocTypes)
- Configuration management (repositories, rules, mappings)
- Employee mapping lookups
- Providing classification rules and scoring matrices
- Storing processed commits in Development Activity Log
- Content opportunity management

#### Process Flow

1. **Initiation (n8n)**
   - Schedule Trigger fires based on configured intervals
   - n8n fetches repository configurations from ERPNext

2. **Collection & Processing (n8n)**
   - Executes git commands to fetch commits between timestamps
   - Parses commit messages and extracts metadata
   - Calculates lines added/removed from git diff
   - Filters bot commits and merge commits using patterns
   - Queries ERPNext for employee mappings
   - Applies classification rules from ERPNext Configuration
   - Calculates impact scores using ERPNext scoring matrix

3. **Data Storage (ERPNext)**
   - n8n sends processed commit data to ERPNext
   - ERPNext stores commits in Development Activity Log DocType
   - Updates Commit Collection Run status

4. **Opportunity Detection (ERPNext)**
   - Identifies high-impact commits (score > threshold)
   - Flags content-worthy items
   - Creates Content Opportunity records

5. **Notification (n8n)**
   - n8n checks for high-impact commits
   - Sends notifications to content team
   - Triggers social media pipeline integration

### n8n Workflow Nodes

#### Core Processing Nodes
1. **Schedule Trigger**: Initiates collection based on configured intervals
2. **HTTP Request**: Fetches repository configurations from ERPNext
3. **Execute Command**: Runs git commands (log, diff, show)
4. **Code Node (JavaScript)**: 
   - Parses git output
   - Extracts commit metadata
   - Filters bot/merge commits
   - Classifies commits by type
   - Calculates impact scores
5. **HTTP Request**: Queries employee mappings from ERPNext
6. **HTTP Request**: Sends processed commits to ERPNext for storage
7. **IF Node**: Checks for high-impact commits
8. **Email/Webhook**: Sends notifications for content opportunities

#### Supporting Nodes
- **Wait Node**: Implements delays for retry logic
- **Loop Node**: Handles batch processing for large repositories
- **Error Trigger**: Catches and handles workflow failures
- **Set Node**: Manages workflow variables and state

### Data Storage (All in ERPNext)

**Configuration DocTypes:**
- Repository Configuration: Git repo settings, branches, paths
- Classification Rule: Patterns for commit type identification
- Business Impact Matrix: Scoring rules and thresholds
- Employee Mapping: Git author to employee relationships

**Transaction DocTypes:**
- Commit Collection Run: Tracks each collection execution
- Development Activity Log: Stores processed commit data
- Content Opportunity: High-impact commits for content creation

### Why This Architecture?

**Separation of Concerns:**
- n8n handles workflow orchestration without business logic
- ERPNext maintains all business rules and data integrity
- Changes to business logic don't require workflow modifications

**Data Consistency:**
- All data remains in ERPNext database
- No data duplication between systems
- Single source of truth for all commit data

**Scalability:**
- n8n can trigger parallel processing for multiple repositories
- ERPNext handles concurrent operations with built-in queue management
- Processing load distributed based on ERPNext server capabilities

## Implementation Approach

### Phase 1: ERPNext Foundation
1. Create all required DocTypes in ERPNext
2. Implement Git operation methods in Repository Configuration
3. Build classification and scoring logic
4. Set up employee mapping system

### Phase 2: n8n Workflow Setup
1. Configure scheduled triggers
2. Create HTTP request nodes for ERPNext calls
3. Set up notification handlers
4. Implement error handling and retry logic

### Phase 3: Integration
1. Test end-to-end workflow
2. Configure content opportunity thresholds
3. Connect to social media pipeline
4. Set up monitoring and alerts

## Integration Points with Existing Content Pipeline

### 1. Content Opportunity Detection
```
┌────────────── Content Opportunity Detection Flow ──────────────┐
│                                                                 │
│   ERPNext      Development       Content          Social       │
│   Collector    Activity Log      Opportunity      Media        │
│     (EC)          (DAL)          Detector(COD)    System(SMS)  │
│      │              │                 │               │        │
│      │              │                 │               │        │
│      │ Store        │                 │               │        │
│      │ processed    │                 │               │        │
│      │ commits      │                 │               │        │
│      ├─────────────▶│                 │               │        │
│      │              │                 │               │        │
│      │              │ Trigger         │               │        │
│      │              │ opportunity     │               │        │
│      │              │ check           │               │        │
│      │              ├────────────────▶│               │        │
│      │              │                 │               │        │
│      │              │                 │ Query         │        │
│      │              │                 │ high-impact   │        │
│      │              │◄────────────────┤ commits       │        │
│      │              │                 │               │        │
│      │              │ Return scored   │               │        │
│      │              │ commits         │               │        │
│      │              ├────────────────▶│               │        │
│      │              │                 │               │        │
│      │              │                 │ Send          │        │
│      │              │                 │ opportunity   │        │
│      │              │                 │ notification  │        │
│      │              │                 ├──────────────▶│        │
│      │              │                 │               │        │
│      │              │                 │               │ Queue  │
│      │              │                 │               │ for    │
│      │              │                 │               │ demo   │
│      │              │                 │               │────┐   │
│      │              │                 │               │    │   │
│      │              │                 │               │◄───┘   │
│      │              │                 │               │        │
│      ▼              ▼                 ▼               ▼        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Demo Session Integration
The system integrates with the existing demo session workflow by:
- Providing commit details for developer context
- Supplying before/after metrics from commit analysis
- Offering proof points and technical details
- Supporting ROI calculation with impact scores

### 3. Content Generation Pipeline
```
┌─────────────────── Content Generation Pipeline ────────────────────┐
│                                                                     │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐    │
│  │ High-Impact  │     │  Developer   │     │ Demo Session   │    │
│  │   Commits    ├────▶│   Outreach   ├────▶│   Scheduled    │    │
│  └──────────────┘     └──────────────┘     └────────┬───────┘    │
│                                                      │            │
│                                                      ▼            │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐    │
│  │Multi-Platform│     │   Quality    │     │Content Capture │    │
│  │ Distribution │◄────┤  Validation  │◄────┤   Session      │    │
│  └──────────────┘     └──────────────┘     └────────────────┘    │
│         ▲                                           │             │
│         │                                           ▼             │
│         │                                   ┌────────────────┐    │
│         └───────────────────────────────────┤Story Creation  │    │
│                                             └────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Business Impact Scoring Algorithm

### Base Score Calculation
```python
def calculate_base_score(commit_type, target_role):
    """Calculate base impact score from Business Impact Matrix"""
    matrix_entry = get_impact_matrix(commit_type, target_role)
    return matrix_entry.base_score

def apply_multipliers(base_score, commit_data):
    """Apply multiplier factors based on commit characteristics"""
    multipliers = {
        'lines_changed': min(commit_data.lines_added + commit_data.lines_removed, 1000) * 0.01,
        'files_affected': min(commit_data.files_changed, 50) * 0.02,
        'customer_facing': 1.2 if is_customer_facing(commit_data.files) else 1.0,
        'critical_path': 1.3 if is_critical_system(commit_data.files) else 1.0,
        'performance_impact': 1.15 if has_performance_keywords(commit_data.message) else 1.0
    }
    
    final_score = base_score
    for factor, value in multipliers.items():
        if factor in ['customer_facing', 'critical_path', 'performance_impact']:
            final_score *= value
        else:
            final_score += value
    
    return min(final_score, 100)  # Cap at 100

def determine_content_worthiness(final_score, commit_type):
    """Determine if commit is worthy of content creation"""
    thresholds = {
        'Feature': 70,
        'Bug Fix': 60,
        'Performance': 65,
        'Security': 80,
        'Refactor': 55,
        'Documentation': 45
    }
    
    return final_score >= thresholds.get(commit_type, 60)
```

### Scoring Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Base Score | 1.0 | From Business Impact Matrix by type/role |
| Lines Changed | 0.01/line | Up to 1000 lines (10 points max) |
| Files Affected | 0.02/file | Up to 50 files (1 point max) |
| Customer Facing | 1.2x | Multiplier for user-facing changes |
| Critical Path | 1.3x | Multiplier for core system changes |
| Performance | 1.15x | Multiplier for performance improvements |

## Use Case Diagrams

```
┌───────────────────── System Use Cases ─────────────────────────┐
│                                                                 │
│  ┌─────────── System Actors ───────────┐                      │
│  │                                      │                      │
│  │  ┌──────────────────────────────┐   │                      │
│  │  │   Content Operations Team    │   │                      │
│  │  └──────────────┬───────────────┘   │                      │
│  │                 │                    │                      │
│  │  ┌──────────────┴───────────────┐   │                      │
│  │  │        Developers            │   │                      │
│  │  └──────────────┬───────────────┘   │                      │
│  │                 │                    │                      │
│  │  ┌──────────────┴───────────────┐   │                      │
│  │  │     System Scheduler         │   │                      │
│  │  └──────────────┬───────────────┘   │                      │
│  │                 │                    │                      │
│  │  ┌──────────────┴───────────────┐   │                      │
│  │  │      Marketing Team          │   │                      │
│  │  └──────────────────────────────┘   │                      │
│  └──────────────────────────────────────┘                      │
│                                                                 │
│  ┌─────────────── Use Cases ───────────────────────────────┐  │
│  │                                                          │  │
│  │  System Scheduler:                                       │  │
│  │  ├─► UC1: Schedule Collection Run                        │  │
│  │  ├─► UC2: Process Commits                                │  │
│  │  ├─► UC3: Classify Commits                               │  │
│  │  ├─► UC4: Map to Employees                               │  │
│  │  ├─► UC5: Score Business Impact                          │  │
│  │  ├─► UC6: Generate Activity Log                          │  │
│  │  └─► UC7: Identify Content Opportunities                 │  │
│  │                                                          │  │
│  │  Content Operations Team:                                │  │
│  │  ├─► UC8: Configure Repositories                         │  │
│  │  ├─► UC9: Manage Employee Mappings                       │  │
│  │  ├─► UC10: Review Failed Collections                     │  │
│  │  └─► UC7: Identify Content Opportunities                 │  │
│  │                                                          │  │
│  │  Developers:                                             │  │
│  │  └─► UC9: Manage Employee Mappings                       │  │
│  │                                                          │  │
│  │  Marketing Team:                                         │  │
│  │  └─► UC7: Identify Content Opportunities                 │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Sequence Diagrams

### Commit Collection and Processing Sequence
```
┌────────────── Commit Collection & Processing Sequence ──────────────┐
│                                                                      │
│  Scheduler  Commit    Repository  Commit    Employee  Classification│
│     (S)     Collector  Manager    Processor  Mapper   Service (CS)  │
│      │       (CC)      (RM)        (CP)      (EM)         │         │
│      │         │         │           │         │           │         │
│      │ Trigger │         │           │         │           │         │
│      │collection│         │           │         │           │         │
│      │ run     │         │           │         │           │         │
│      ├────────▶│         │           │         │           │         │
│      │         │         │           │         │           │         │
│      │         │Get active│           │         │           │         │
│      │         │repos    │           │         │           │         │
│      │         ├────────▶│           │         │           │         │
│      │         │         │           │         │           │         │
│      │         │◄────────┤           │         │           │         │
│      │         │ Repo    │           │         │           │         │
│      │         │ configs │           │         │           │         │
│      │         │         │           │         │           │         │
│  ┌───┴─────────┴─────────┴───────────┴─────────┴───────────┴───┐    │
│  │                    For each repository                       │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │ Fetch   │           │         │           │    │    │
│  │  │         │commits  │           │         │           │    │    │
│  │  │         │(T0-T1)  │           │         │           │    │    │
│  │  │         ├────────▶│           │         │           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │◄────────┤           │         │           │    │    │
│  │  │         │Raw commit│           │         │           │    │    │
│  │  │         │ data    │           │         │           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │Process  │           │         │           │    │    │
│  │  │         │raw      │           │         │           │    │    │
│  │  │         │commits  │           │         │           │    │    │
│  │  │         ├────────────────────▶│         │           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │         │           │Filter   │           │    │    │
│  │  │         │         │           │bots/    │           │    │    │
│  │  │         │         │           │merges   │           │    │    │
│  │  │         │         │           ├────┐    │           │    │    │
│  │  │         │         │           │    │    │           │    │    │
│  │  │         │         │           │◄───┘    │           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │         │           │Map to   │           │    │    │
│  │  │         │         │           │employees│           │    │    │
│  │  │         │         │           ├────────▶│           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │         │           │◄────────┤           │    │    │
│  │  │         │         │           │Employee │           │    │    │
│  │  │         │         │           │mappings │           │    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │         │           │Classify │           │    │    │
│  │  │         │         │           │commit   │           │    │    │
│  │  │         │         │           │types    │           │    │    │
│  │  │         │         │           ├────────────────────▶│    │    │
│  │  │         │         │           │         │           │    │    │
│  │  │         │         │           │◄────────────────────┤    │    │
│  │  │         │         │           │Classifications      │    │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                      │
│      │         │         │           │         │           │         │
│      │         │         │           │Calculate│           │         │
│      │         │         │           │impact   │           │         │
│      │         │         │           │scores──▶│Impact     │         │
│      │         │         │           │         │Scorer(IS) │         │
│      │         │         │           │◄────────┤           │         │
│      │         │         │           │Impact   │           │         │
│      │         │         │           │scores   │           │         │
│      │         │         │           │         │           │         │
│      │         │         │           │Store    │           │         │
│      │         │         │           │commits─▶│Development │         │
│      │         │         │           │         │Activity   │         │
│      │         │         │           │         │Log (DAL)  │         │
│      │         │         │           │         │           │         │
│      │◄─────────────────────────────────────────┤           │         │
│      │Collection complete                       │           │         │
│      │         │         │           │         │           │         │
│      │Update   │         │           │         │           │         │
│      │T0 = T1  │         │           │         │           │         │
│      ├────┐    │         │           │         │           │         │
│      │    │    │         │           │         │           │         │
│      │◄───┘    │         │           │         │           │         │
│      ▼         ▼         ▼           ▼         ▼           ▼         │
└──────────────────────────────────────────────────────────────────────┘
```

### Content Opportunity Detection Sequence
```
┌───────────── Content Opportunity Detection Sequence ────────────────┐
│                                                                      │
│  Development   Content      Notification  Social     Content        │
│  Activity Log  Opportunity  Engine       Media      Operations      │
│  (DAL)         Detector(COD) (NE)        System(SMS) (CO)           │
│     │             │            │            │           │           │
│     │ New high-   │            │            │           │           │
│     │ impact      │            │            │           │           │
│     │ commit      │            │            │           │           │
│     │ stored      │            │            │           │           │
│     ├────────────▶│            │            │           │           │
│     │             │            │            │           │           │
│     │             │Query       │            │           │           │
│     │             │related     │            │           │           │
│     │◄────────────┤commits     │            │           │           │
│     │             │            │            │           │           │
│     │ Commit      │            │            │           │           │
│     │ context     │            │            │           │           │
│     ├────────────▶│            │            │           │           │
│     │             │            │            │           │           │
│     │             │Evaluate    │            │           │           │
│     │             │content     │            │           │           │
│     │             │potential   │            │           │           │
│     │             ├────┐       │            │           │           │
│     │             │    │       │            │           │           │
│     │             │◄───┘       │            │           │           │
│     │             │            │            │           │           │
│     │             │Send        │            │           │           │
│     │             │opportunity │            │           │           │
│     │             │alert       │            │           │           │
│     │             ├───────────▶│            │           │           │
│     │             │            │            │           │           │
│     │             │            │Queue       │           │           │
│     │             │            │content     │           │           │
│     │             │            │opportunity │           │           │
│     │             │            ├───────────▶│           │           │
│     │             │            │            │           │           │
│     │             │            │            │Notify team│           │
│     │             │            │            │of         │           │
│     │             │            │            │opportunity│           │
│     │             │            │            ├──────────▶│           │
│     │             │            │            │           │           │
│     │             │            │            │           │Schedule   │
│     │             │            │            │           │demo       │
│     │             │            │            │◄──────────┤session    │
│     │             │            │            │           │           │
│     ▼             ▼            ▼            ▼           ▼           │
└──────────────────────────────────────────────────────────────────────┘
```

## State Diagrams for Commit Processing

```
┌──────────────── Commit Processing State Machine ────────────────────┐
│                                                                      │
│     ┌─────────┐                                                     │
│     │  Start  │                                                     │
│     └────┬────┘                                                     │
│          │                                                          │
│          ▼                                                          │
│     ┌─────────┐         Start            ┌────────────┐            │
│     │   Raw   ├────── Processing ───────▶│ Filtering  │            │
│     └─────────┘                          └─────┬──────┘            │
│                                                 │                    │
│                              ┌──────────────────┼──────────────────┐│
│                              │                  │                  ││
│                   Bots/Merges│                  │Bot/Merge         ││
│                       Removed│                  │Detected          ││
│                              ▼                  ▼                  ││
│                        ┌──────────┐       ┌────────────┐           ││
│                        │ Filtered │       │ Discarded  ├───────┐   ││
│                        └─────┬────┘       └────────────┘       │   ││
│                              │                                  │   ││
│                     Employee │                                  │   ││
│                       Lookup │                                  │   ││
│                              ▼                                  │   ││
│                        ┌──────────┐                            │   ││
│                        │ Mapping  │                            │   ││
│                        └─────┬────┘                            │   ││
│                              │                                  │   ││
│                ┌─────────────┼─────────────┐                   │   ││
│                │             │             │                   │   ││
│       Employee │             │    Employee │                   │   ││
│          Found │             │   Not Found │                   │   ││
│                ▼             │             ▼                   │   ││
│          ┌──────────┐        │      ┌──────────────┐          │   ││
│          │  Mapped  │        │      │ UnmappedReview│          │   ││
│          └─────┬────┘        │      └──────┬───────┘          │   ││
│                │              │             │                   │   ││
│                │              │    ┌────────┼────────┐         │   ││
│                │              │    │        │        │         │   ││
│                │              │Manual      Invalid   │         │   ││
│                │              │Mapping      Author   │         │   ││
│                │              │    │        │        │         │   ││
│                │              └────┘        ▼        │         │   ││
│                │                      (Discarded)    │         │   ││
│                │                                     │         │   ││
│          Type  │                                     │         │   ││
│       Analysis │                                     │         │   ││
│                ▼                                     │         │   ││
│         ┌──────────────┐                            │         │   ││
│         │ Classifying  │                            │         │   ││
│         └──────┬───────┘                            │         │   ││
│                │                                     │         │   ││
│     ┌──────────┼──────────┐                        │         │   ││
│     │          │          │                        │         │   ││
│  Type       Classification│                        │         │   ││
│ Assigned      Uncertain   │                        │         │   ││
│     │          │          │                        │         │   ││
│     ▼          ▼          │                        │         │   ││
│ ┌──────────┐ ┌────────────┐                       │         │   ││
│ │Classified│ │ManualReview│                       │         │   ││
│ └────┬─────┘ └─────┬──────┘                       │         │   ││
│      │             │                               │         │   ││
│      │    ┌────────┼────────┐                     │         │   ││
│      │    │        │        │                     │         │   ││
│      │  Manual   Invalid    │                     │         │   ││
│      │Classification Commit │                     │         │   ││
│      │    │        │        │                     │         │   ││
│      │    ▼        ▼        │                     │         │   ││
│      │ (Classified)(Discarded)                    │         │   ││
│      │                                            │         │   ││
│   Impact                                          │         │   ││
│Calculation                                        │         │   ││
│      ▼                                            │         │   ││
│ ┌──────────┐                                      │         │   ││
│ │ Scoring  │                                      │         │   ││
│ └────┬─────┘                                      │         │   ││
│      │                                            │         │   ││
│  Score                                            │         │   ││
│ Assigned                                          │         │   ││
│      ▼                                            │         │   ││
│ ┌──────────┐                                      │         │   ││
│ │  Scored  │                                      │         │   ││
│ └────┬─────┘                                      │         │   ││
│      │                                            │         │   ││
│  Check                                            │         │   ││
│ Content                                           │         │   ││
│  Worth                                            │         │   ││
│      ▼                                            │         │   ││
│ ┌──────────────────┐                             │         │   ││
│ │ContentEvaluation │                             │         │   ││
│ └────────┬─────────┘                             │         │   ││
│          │                                        │         │   ││
│  ┌───────┼────────┐                              │         │   ││
│  │       │        │                              │         │   ││
│Score > Score <    │                              │         │   ││
│Threshold Threshold│                              │         │   ││
│  │       │        │                              │         │   ││
│  ▼       ▼        │                              │         │   ││
│┌──────────────┐┌──────────┐                     │         │   ││
││ContentWorthy ││ Archived │                     │         │   ││
│└──────┬───────┘└────┬─────┘                     │         │   ││
│       │             │                            │         │   ││
│  High │             │                            │         │   ││
│Impact │             │                            │         │   ││
│       ▼             │                            │         │   ││
│┌──────────────────┐│                            │         │   ││
││OpportunityQueue  ││                            │         │   ││
│└──────┬───────────┘│                            │         │   ││
│       │             │                            │         │   ││
│       └─────────────┼────────────────────────────┼─────────┘   ││
│                     │                            │             ││
│                     ▼                            ▼             ││
│                ┌─────────┐                                     ││
│                │   End   │                                     ││
│                └─────────┘                                     ││
└──────────────────────────────────────────────────────────────────┘
```

## Entity Relationship Diagrams

```
┌──────────────────── Entity Relationship Diagram ────────────────────┐
│                                                                      │
│  ┌───────────────────────────┐         ┌──────────────────────┐    │
│  │ REPOSITORY-CONFIGURATION  │         │ COMMIT-COLLECTION-RUN│    │
│  ├───────────────────────────┤         ├──────────────────────┤    │
│  │ • name (PK)               │ 1     * │ • name (PK)          │    │
│  │ • repo_path               ├─────────┤ • repository_config  │    │
│  │ • branch                  │generates│   (FK)               │    │
│  │ • is_active               │         │ • start_timestamp    │    │
│  │ • collection_frequency    │         │ • end_timestamp      │    │
│  │ • created                 │         │ • status             │    │
│  └───────────────────────────┘         │ • commits_processed  │    │
│                                         │ • created            │    │
│                                         └──────────┬───────────┘    │
│                                                    │ 1              │
│                                                    │                │
│                                                    │ contains      │
│                                                    │                │
│                                                    │ *              │
│  ┌───────────────────────────┐         ┌──────────▼───────────┐    │
│  │    EMPLOYEE-MAPPING       │         │ DEVELOPMENT-ACTIVITY │    │
│  ├───────────────────────────┤         │         LOG          │    │
│  │ • name (PK)               │ 1     * ├──────────────────────┤    │
│  │ • employee (FK)           ├─────────┤ • name (PK)          │    │
│  │ • employee_name           │ maps-to │ • commit_hash        │    │
│  │ • git_email               │         │ • repository         │    │
│  │ • git_name                │         │ • branch             │    │
│  │ • alternative_emails      │         │ • author_name        │    │
│  │ • is_active               │         │ • author_email       │    │
│  │ • created                 │         │ • employee (FK)      │    │
│  └───────────────────────────┘         │ • commit_message     │    │
│                                         │ • timestamp          │    │
│  ┌───────────────────────────┐         │ • files_changed      │    │
│  │   CLASSIFICATION-RULE     │         │ • lines_added        │    │
│  ├───────────────────────────┤         │ • lines_removed      │    │
│  │ • name (PK)               │ 1     * │ • classification     │    │
│  │ • pattern                 ├─────────┤ • classification_    │    │
│  │ • commit_type             │classifies  confidence         │    │
│  │ • keywords                │         │ • business_impact_   │    │
│  │ • weight                  │         │   score              │    │
│  │ • is_active               │         │ • target_roles       │    │
│  │ • created                 │         │ • content_worthy     │    │
│  └───────────────────────────┘         │ • collection_run(FK) │    │
│                                         │ • created            │    │
│  ┌───────────────────────────┐         └──────────┬───────────┘    │
│  │  BUSINESS-IMPACT-MATRIX   │                    │ 1              │
│  ├───────────────────────────┤                    │                │
│  │ • name (PK)               │ 1     *            │ derives-from   │
│  │ • commit_type             ├─────────scores     │                │
│  │ • target_role             │                    │ *              │
│  │ • base_score              │         ┌──────────▼───────────┐    │
│  │ • multiplier_factors      │         │  CONTENT-OPPORTUNITY │    │
│  │ • content_threshold       │         ├──────────────────────┤    │
│  │ • is_active               │         │ • name (PK)          │    │
│  │ • created                 │         │ • activity_log (FK)  │    │
│  └───────────────────────────┘         │ • opportunity_type   │    │
│                                         │ • priority_score     │    │
│                                         │ • status             │    │
│                                         │ • identified_on      │    │
│                                         │ • assigned_to        │    │
│                                         │ • demo_scheduled     │    │
│                                         │ • created            │    │
│                                         └──────────────────────┘    │
│                                                                      │
│  Relationships:                                                      │
│  ──────────────                                                      │
│  1:* = One to Many relationship                                      │
│  PK = Primary Key                                                    │
│  FK = Foreign Key                                                    │
└──────────────────────────────────────────────────────────────────────┘
```

## User Stories and Acceptance Criteria

### Epic 1: Automated Commit Collection

**Story 1.1**: As a Content Operations Manager, I want to schedule automated commit collection runs so that development activities are continuously captured without manual intervention.

**Acceptance Criteria**:
- Given a repository configuration exists
- When I schedule a collection run
- Then the system collects all commits between T0 and T1
- And updates T0 to current T1 for next run
- And logs the collection results

**Story 1.2**: As a Content Operations Team member, I want to monitor collection run status so that I can ensure data integrity and troubleshoot issues.

**Acceptance Criteria**:
- Given collection runs are executing
- When I view the collection run dashboard
- Then I see real-time status updates
- And error logs for failed runs
- And retry options for failed collections

### Epic 2: Intelligent Commit Analysis

**Story 2.1**: As a Content Creator, I want commits automatically classified by type so that I can quickly identify content opportunities.

**Acceptance Criteria**:
- Given raw commit data is collected
- When the classification service processes commits
- Then each commit receives an accurate type classification
- And classification confidence scores are provided
- And uncertain classifications are flagged for review

**Story 2.2**: As a Marketing Team Lead, I want business impact scores for commits so that I can prioritize content creation efforts.

**Acceptance Criteria**:
- Given classified commits exist
- When impact scoring is applied
- Then each commit receives a score from 1-100
- And scores consider target audience relevance
- And high-scoring commits are flagged as content-worthy

### Epic 3: Employee Attribution

**Story 3.1**: As a Content Operations Manager, I want Git authors mapped to employees so that I can attribute content to the right people.

**Acceptance Criteria**:
- Given commit author information exists
- When employee mapping is performed
- Then Git emails are matched to employee records
- And multiple Git identities per employee are supported
- And unmatched authors are flagged for manual review

### Epic 4: Content Pipeline Integration

**Story 4.1**: As a Content Creator, I want automatic notifications of content opportunities so that I can quickly engage developers for demo sessions.

**Acceptance Criteria**:
- Given high-impact commits are identified
- When content opportunity detection runs
- Then relevant team members receive notifications
- And commit context is provided for outreach
- And integration with demo scheduling system works

## Success Metrics

### Primary KPIs
| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Collection Success Rate | >99% | Successful runs / Total runs |
| Classification Accuracy | >85% | Manual validation of sample |
| Content Discovery Rate | 3-5 opportunities/week | High-score commits identified |
| Time to Content Creation | <48 hours | From commit to demo scheduled |
| Employee Mapping Rate | >95% | Mapped commits / Total commits |

### Secondary KPIs
| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| System Uptime | >99.5% | Monitoring dashboard |
| Processing Speed | <5 min per 10K commits | Performance logs |
| False Positive Rate | <10% | Content team feedback |
| Bot Filtering Accuracy | >98% | Manual audit of filtered commits |
| API Response Time | <2 seconds | Performance monitoring |

### Business Impact Metrics
| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Content Production Increase | +200% | Content pieces published |
| Developer Engagement Rate | >70% | Demo participation rate |
| Social Media Reach | +150% | Platform analytics |
| Lead Generation | +100% | Content-driven inquiries |
| Content Team Efficiency | +80% | Hours saved on discovery |

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
**Objective**: Build core collection and storage infrastructure

**Deliverables**:
- [ ] Repository Configuration DocType and UI
- [ ] Basic Commit Collector service
- [ ] Development Activity Log DocType
- [ ] Employee Mapping DocType and basic matching
- [ ] Commit Collection Run DocType and scheduling
- [ ] Basic API endpoints for manual triggers

**Success Criteria**:
- System can collect commits from configured repositories
- Basic storage and retrieval functionality works
- Manual collection runs execute successfully

### Phase 2: Intelligence Layer (Weeks 5-8)
**Objective**: Implement classification and scoring algorithms

**Deliverables**:
- [ ] Classification Rule engine and DocType
- [ ] Automated commit type classification
- [ ] Business Impact Matrix DocType
- [ ] Impact scoring algorithm implementation
- [ ] Bot and merge filtering logic
- [ ] Enhanced employee mapping with fuzzy matching

**Success Criteria**:
- Classification accuracy >80% on test dataset
- Impact scoring produces meaningful rankings
- Bot filtering removes >95% of automated commits
- Employee mapping rate >90%

### Phase 3: Content Integration (Weeks 9-12)
**Objective**: Integrate with existing content pipeline

**Deliverables**:
- [ ] Content Opportunity Detector service
- [ ] Integration APIs for social media system
- [ ] Notification engine for high-impact commits
- [ ] Dashboard for content team opportunity review
- [ ] Automated scheduling integration
- [ ] Performance monitoring and alerting

**Success Criteria**:
- Content opportunities automatically detected and queued
- Integration with demo scheduling works seamlessly
- Content team adoption >80%
- End-to-end workflow from commit to content creation

### Phase 4: Optimization & Scale (Weeks 13-16)
**Objective**: Optimize performance and add advanced features

**Deliverables**:
- [ ] Performance optimization for large repositories
- [ ] Advanced classification using ML models
- [ ] Bulk operations and data management tools
- [ ] Analytics and reporting dashboard
- [ ] Configuration management UI
- [ ] Comprehensive documentation and training materials

**Success Criteria**:
- System handles 100K+ commits efficiently
- Classification accuracy >85%
- Full feature adoption by all teams
- Documentation complete and team trained

## Risk Assessment and Mitigation

### High-Risk Items
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Git access permissions | High | Medium | Implement secure token management, test access early |
| Classification accuracy | High | Medium | Use hybrid rule-based + ML approach, continuous training |
| Integration complexity | Medium | High | Phased integration, extensive API testing |
| Performance with large repos | High | Medium | Implement pagination, caching, and parallel processing |

### Medium-Risk Items
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Employee mapping gaps | Medium | Medium | Manual review process, bulk import tools |
| Bot detection false positives | Medium | Low | Configurable rules, whitelist management |
| System reliability | Medium | Low | Comprehensive testing, monitoring, alerting |

## Appendices

### Appendix A: Technical Architecture Details

#### Collection Engine Components
```python
class CommitCollector:
    """Main service for collecting commits from repositories"""
    
    def collect_commits(self, repo_config, start_time, end_time):
        """Collect commits between timestamps"""
        pass
    
    def process_commit_batch(self, commits):
        """Process batch of raw commits"""
        pass

class CommitClassifier:
    """Service for classifying commit types"""
    
    def classify_commit(self, commit_data):
        """Classify single commit"""
        pass
    
    def get_classification_confidence(self, commit_data, classification):
        """Calculate confidence score"""
        pass

class ImpactScorer:
    """Service for calculating business impact scores"""
    
    def calculate_impact_score(self, commit_data, classification):
        """Calculate impact score"""
        pass
```

### Appendix B: Configuration Examples

#### Repository Configuration
```json
{
  "name": "ERPNext Main",
  "repo_path": "/home/frappe/frappe-bench/apps/erpnext/.git",
  "branch": "develop",
  "collection_frequency": "daily",
  "is_active": 1,
  "filters": {
    "exclude_paths": ["*.md", "tests/", "docs/"],
    "include_authors": ["@company.com"]
  }
}
```

#### Classification Rules
```json
{
  "name": "Feature Detection",
  "pattern": "^(feat|add|implement)",
  "commit_type": "Feature",
  "keywords": ["feature", "add", "implement", "new"],
  "weight": 0.9
}
```

---

**Document Control**
- Version: 1.0
- Last Updated: 2024-09-04
- Review Frequency: Quarterly
- Owner: Product Management
- Approver: Technical Lead
- Next Review Date: 2024-12-04
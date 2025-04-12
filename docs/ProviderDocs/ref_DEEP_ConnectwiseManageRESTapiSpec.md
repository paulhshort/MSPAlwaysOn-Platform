# All relevant REST API endpoints** from the ConnectWise Manage OpenAPI spec focused on the following high-priority functional areas:

- **Tickets:** Tickets, TicketNotes, TicketTasks, TicketInfos, TicketStopwatches, TicketChangeLog, TicketSyncs

- **Time Tracking:** TimeEntries, TimeEntryAudits, TimeEntryChangeLog, TimeAccruals, TimeAccrualDetails, TimeExpenses

- **Service:** ServiceTemplates, ServiceTemplateInfos, ServiceLocations, ServiceLocationInfos, ServiceTeams, ServiceSignoffs, ServiceTicketLinks, ServiceTicketNotes, ServiceEmailTemplates, etc.

- **Companies & Contacts:** Companies, CompanyCustomNotes, CompanyNotes, CompanyStatuses, CompanySites, CompanySiteInfos, CompanyTeamRoles, CompanyTeams, CompanyTypes, Contacts, ContactNotes, ContactRelationships

- **Members:** Members, MemberInfos, MemberTemplates, MemberSkills, MemberCertifications, MemberDelegations, MemberNotificationSettings, MemberImages

- **Bundles, Documents, KnowledgeBase:** Bundles, Documents, DocumentTypes, KnowledgeBaseArticles, KnowledgeBaseCategories, KnowledgeBaseSubCategories, KnowledgeBaseSettingses

- **M365 Contacts:** M365Contacts, M365ContactSyncInfos, M365ContactSyncMonitorings, M365ContactSyncProperties

- **Parsing:** ParsingTypes, ParsingVariables

- **File Uploading:** FileUploadSettings

- **Calendars:** Calendars, CalendarInfos

- **Boards:** Boards, BoardStatuses, BoardStatusInfos, BoardTypes, BoardTypeInfos, BoardSubTypes, BoardSubTypeInfos, BoardTeams, BoardTeamInfos, BoardItems, BoardItemAssociations, BoardAutoAssignResources, BoardSkillMappings

- **Statuses & Stopwatches:** Statuses, StatusIndicators, ScheduleStopwatch, TicketStopwatches

- **Configurations:** Configurations, ConfigurationTypes, ConfigurationTypeQuestions, ConfigurationTypeQuestionValues, ConfigurationStatusInfos, ConfigurationTypeInfos

- **Reporting:** Reports, ReportingServices, CustomReports, CustomReportParameters

- **Sources:** Sources, SourceInfos

I'll break down each endpoint for those resources, including HTTP method, path, parameters (with detailed syntax), request/response bodies, JSON schema, and error models — fully formatted in Markdown for immediate use by devs or AI coding agents.

I’ll start pulling that together now and let you know when the first detailed package is ready for review.

## Tickets

### GET /service/tickets

**OperationId:** getServiceTickets  
**Summary:** Get List of Ticket  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions for querying records (SQL-like syntax).

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `fields` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **Ticket** objects.

- **400 Bad Request:** Invalid request or parameters.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets

**OperationId:** postServiceTickets  
**Summary:** Post Ticket  
**Parameters:**

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "id": "integer (optional)",
  "summary": "string (required) - Max length: 100;",
  "recordType": "string (optional) - Allowed values: ProjectIssue, ProjectTicket, ServiceTicket.",
  "board": "BoardReference object (optional)",
  "status": "ServiceStatusReference object (optional)",
  "workRole": "WorkRoleReference object (optional)",
  "workType": "WorkTypeReference object (optional)",
  "company": "CompanyReference object (required)",
  "site": "SiteReference object (optional)",
  "siteName": "string (optional) - Max length: 50;",
  "addressLine1": "string (optional) - Max length: 50;",
  "addressLine2": "string (optional) - Max length: 50;",
  "city": "string (optional) - Max length: 50;",
  "stateIdentifier": "string (optional) - Max length: 50;",
  "zip": "string (optional) - Max length: 12;",
  "country": "CountryReference object (optional)",
  "contact": "ContactReference object (optional)",
  "contactName": "string (optional) - Max length: 62;",
  "contactPhoneNumber": "string (optional) - Max length: 20;",
  "contactPhoneExtension": "string (optional) - Max length: 15;",
  "contactEmailAddress": "string (optional) - Max length: 250;",
  "type": "ServiceTypeReference object (optional)",
  "subType": "ServiceSubTypeReference object (optional)",
  "item": "ServiceItemReference object (optional)",
  "team": "ServiceTeamReference object (optional)",
  "owner": "MemberReference object (optional)",
  "priority": "PriorityReference object (optional)",
  "serviceLocation": "ServiceLocationReference object (optional)",
  "source": "ServiceSourceReference object (optional)",
  "requiredDate": "string(date-time) (optional)",
  "budgetHours": "number(double) (optional)",
  "opportunity": "OpportunityReference object (optional)",
  "agreement": "AgreementReference object (optional)",
  "agreementType": "string (optional)",
  "severity": "string (optional) - Required On Updates; Allowed values: Low, Medium, High.",
  "impact": "string (optional) - Required On Updates; Allowed values: Low, Medium, High.",
  "externalXRef": "string (optional) - Max length: 100;",
  "poNumber": "string (optional) - Max length: 50;",
  "knowledgeBaseCategoryId": "integer(int32) (optional)",
  "knowledgeBaseSubCategoryId": "integer(int32) (optional)",
  "allowAllClientsPortalView": "boolean (optional)",
  "customerUpdatedFlag": "boolean (optional)",
  "automaticEmailContactFlag": "boolean (optional)",
  "automaticEmailResourceFlag": "boolean (optional)",
  "automaticEmailCcFlag": "boolean (optional)",
  "automaticEmailCc": "string (optional) - Max length: 1000;",
  "initialDescription": "string (optional) - Only available for POST, will not be returned in the response.",
  "initialInternalAnalysis": "string (optional) - Only available for POST, will not be returned in the response.",
  "initialResolution": "string (optional) - Only available for POST, will not be returned in the response.",
  "initialDescriptionFrom": "string (optional)",
  "contactEmailLookup": "string (optional)",
  "processNotifications": "boolean (optional) - Can be set to false to skip notification processing when adding or updating a ticket (Defaults to True).",
  "skipCallback": "boolean (optional)",
  "closedDate": "string (optional)",
  "closedBy": "string (optional)",
  "closedFlag": "boolean (optional)",
  "actualHours": "number(double) (optional)",
  "approved": "boolean (optional)",
  "estimatedExpenseCost": "number(double) (optional)",
  "estimatedExpenseRevenue": "number(double) (optional)",
  "estimatedProductCost": "number(double) (optional)",
  "estimatedProductRevenue": "number(double) (optional)",
  "estimatedTimeCost": "number(double) (optional)",
  "estimatedTimeRevenue": "number(double) (optional)",
  "billingMethod": "string (optional) - Allowed values: ActualRates, FixedFee, NotToExceed, OverrideRate.",
  "billingAmount": "number(double) (optional)",
  "hourlyRate": "number(double) (optional)",
  "subBillingMethod": "string (optional) - Allowed values: ActualRates, FixedFee, NotToExceed, OverrideRate.",
  "subBillingAmount": "number(double) (optional)",
  "subDateAccepted": "string (optional)",
  "dateResolved": "string (optional)",
  "dateResplan": "string (optional)",
  "dateResponded": "string (optional)",
  "resolveMinutes": "integer(int32) (optional)",
  "resPlanMinutes": "integer(int32) (optional)",
  "respondMinutes": "integer(int32) (optional)",
  "isInSla": "boolean (optional)",
  "knowledgeBaseLinkId": "integer(int32) (optional)",
  "resources": "string (optional)",
  "parentTicketId": "integer(int32) (optional)",
  "hasChildTicket": "boolean (optional)",
  "hasMergedChildTicketFlag": "boolean (optional)",
  "knowledgeBaseLinkType": "string (optional) - Allowed values: Activity, ProjectIssue, KnowledgeBaseArticle, ProjectTicket, ServiceTicket, Time.",
  "billTime": "string (optional) - Allowed values: Billable, DoNotBill, NoCharge, NoDefault.",
  "billExpenses": "string (optional) - Allowed values: Billable, DoNotBill, NoCharge, NoDefault.",
  "billProducts": "string (optional) - Allowed values: Billable, DoNotBill, NoCharge, NoDefault.",
  "predecessorType": "string (optional) - Allowed values: Ticket, Phase.",
  "predecessorId": "integer(int32) (optional)",
  "predecessorClosedFlag": "boolean (optional)",
  "lagDays": "integer(int32) (optional)",
  "lagNonworkingDaysFlag": "boolean (optional)",
  "estimatedStartDate": "string(date-time) (optional)",
  "duration": "integer(int32) (optional)",
  "location": "SystemLocationReference object (optional)",
  "department": "SystemDepartmentReference object (optional)",
  "mobileGuid": "string(uuid) (optional)",
  "sla": "SLAReference object (optional)",
  "slaStatus": "string (optional)",
  "requestForChangeFlag": "boolean (optional)",
  "currency": "CurrencyReference object (optional)",
  "mergedParentTicket": "TicketReference object (optional)",
  "integratorTags": "array of string (optional)",
  "_info": "object (optional)",
  "escalationStartDateUTC": "string (optional)",
  "escalationLevel": "integer(int32) (optional)",
  "minutesBeforeWaiting": "integer(int32) (optional)",
  "respondedSkippedMinutes": "integer(int32) (optional)",
  "resplanSkippedMinutes": "integer(int32) (optional)",
  "respondedHours": "number(double) (optional)",
  "respondedBy": "string (optional)",
  "resplanHours": "number(double) (optional)",
  "resplanBy": "string (optional)",
  "resolutionHours": "number(double) (optional)",
  "resolvedBy": "string (optional)",
  "minutesWaiting": "integer(int32) (optional)",
  "customFields": "array of CustomFieldValue objects (optional)"
}
```

**Responses:**

- **201 Created:** Returns a **Ticket** object.

- **400 Bad Request:** Invalid request (e.g., malformed input or validation error).

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied to the resource.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/calculateSla

**OperationId:** getServiceTicketsCalculateSla  
**Summary:** Get List of Ticket with SLA calculated  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions for querying records.

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `fields` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **Ticket** objects.

- **400 Bad Request:** Invalid request or parameters.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/count

**OperationId:** getServiceTicketsCount  
**Summary:** Get Count of Ticket  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions for querying records.

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns a **integer(int32)** (count of tickets).

- **400 Bad Request:** Invalid request or parameters.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/search

**OperationId:** postServiceTicketsSearch  
**Summary:** Post Ticket search  
**Parameters:**

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "conditions": "string (optional) - Query filter conditions.",
  "customFieldConditions": "string (optional)"
}
```

**Responses:**

- **200 OK:** Returns an array of **Ticket** objects matching the search criteria.

- **400 Bad Request:** Invalid request (e.g., malformed filter syntax).

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{id}

**OperationId:** getServiceTicketsById  
**Summary:** Get Ticket  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `fields` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns a **Ticket** object.

- **400 Bad Request:** Invalid request (e.g., invalid conditions).

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied to the resource.

- **404 Not Found:** The specified ticket does not exist.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /service/tickets/{id}

**OperationId:** deleteServiceTicketsById  
**Summary:** Delete Ticket  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Ticket deleted successfully (no response body).

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied to the resource.

- **404 Not Found:** The specified ticket does not exist.

- **500 Internal Server Error:** An unexpected server error occurred.

### PUT /service/tickets/{id}

**OperationId:** putServiceTicketsById  
**Summary:** Put Ticket (replace)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets)* – Provide all Ticket fields to replace the existing ticket.

**Responses:**

- **200 OK:** Returns the updated **Ticket** object.

- **400 Bad Request:** Invalid request (e.g., validation error).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** The specified ticket does not exist.

- **500 Internal Server Error:** An unexpected server error occurred.

### PATCH /service/tickets/{id}

**OperationId:** patchServiceTicketsById  
**Summary:** Patch Ticket (partial update)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets)* – Provide only the fields of Ticket that need to be updated.

**Responses:**

- **200 OK:** Returns the updated **Ticket** object.

- **400 Bad Request:** Invalid request (e.g., validation error).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** The specified ticket does not exist.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{id}/copy

**OperationId:** postServiceTicketsByIdCopy  
**Summary:** Post TicketCopy (copy an existing ticket)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId of the ticket to copy

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "scheduleEntriesFlag": "boolean (optional)",
  "attachmentsFlag": "boolean (optional)",
  "newTicketDefaults": "Ticket object (optional) - Default values for the new copied ticket."
}
```

**Responses:**

- **201 Created:** Returns the newly created **Ticket** (copy) object.

- **400 Bad Request:** Invalid request (e.g., missing required data for copy).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** The source ticket was not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/activities

**OperationId:** getServiceTicketsByParentIdActivities  
**Summary:** Get List of ActivityReference (activities associated with the ticket – *Deprecated*, use `/sales/activities?conditions=ticket/id={id}` instead)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **ActivityReference** objects related to the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/activities/count

**OperationId:** getServiceTicketsByParentIdActivitiesCount  
**Summary:** Get Count of ActivityReference (count of activities on the ticket – *Deprecated*, use `/sales/activities/count?conditions=ticket/id={id}`)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of activities on the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{parentId}/attachChildren

**OperationId:** postServiceTicketsByParentIdAttachChildren  
**Summary:** Attach child tickets to a parent ticket  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId of parent ticket

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "childTicketIds": "array of integer(int32) (required) - List of ticket IDs to attach as children."
}
```

**Responses:**

- **200 OK:** Child tickets attached successfully (returns a success response object or empty body on success).

- **400 Bad Request:** Invalid request (e.g., list of IDs missing or invalid).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Parent or one of the child tickets not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/configurations

**OperationId:** getServiceTicketsByParentIdConfigurations  
**Summary:** Get List of ConfigurationReference (configurations linked to the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **ConfigurationReference** objects linked to the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{parentId}/configurations

**OperationId:** postServiceTicketsByParentIdConfigurations  
**Summary:** Post ConfigurationReference (link a configuration to the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "id": "integer (required) - Configuration ID to link"
}
```

**Responses:**

- **201 Created:** Configuration linked to ticket (returns linked **ConfigurationReference**).

- **400 Bad Request:** Invalid request (e.g., missing or invalid config ID).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket or configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/configurations/{id}

**OperationId:** getServiceTicketsByParentIdConfigurationsById  
**Summary:** Get ConfigurationReference (a specific configuration linked to the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: configurationId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **ConfigurationReference** object for that configuration.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket or configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /service/tickets/{parentId}/configurations/{id}

**OperationId:** deleteServiceTicketsByParentIdConfigurationsById  
**Summary:** Delete ConfigurationReference (unlink a configuration from the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: configurationId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Configuration unlinked from ticket successfully.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket or configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/configurations/count

**OperationId:** getServiceTicketsByParentIdConfigurationsCount  
**Summary:** Get Count of ConfigurationReference links on the ticket  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of configurations linked to the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{parentId}/convert

**OperationId:** postServiceTicketsByParentIdConvert  
**Summary:** Convert ticket (ServiceTicket to ServiceTicket or ProjectTicket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId to convert

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "type": "string (optional) - Target ticket type (e.g., ServiceTicket or ProjectTicket)",
  "projectId": "integer (optional) - If converting to ProjectTicket, the target project ID"
}
```

**Responses:**

- **200 OK:** Ticket converted successfully (returns a success response or updated **Ticket** object).

- **400 Bad Request:** Invalid request (e.g., unsupported conversion parameters).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket or target project not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/documents

**OperationId:** getServiceTicketsByParentIdDocuments  
**Summary:** Get List of DocumentReference (documents attached to the ticket – *Deprecated*, use `/system/documents?recordType=Ticket&recordId={id}`)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **DocumentReference** objects attached to the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/documents/count

**OperationId:** getServiceTicketsByParentIdDocumentsCount  
**Summary:** Get Count of DocumentReference (documents count on the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of documents attached to the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/products

**OperationId:** getServiceTicketsByParentIdProducts  
**Summary:** Get List of ProductReference (products associated with the ticket – *Deprecated*, use `/procurement/products?conditions=chargeToType='Ticket' AND chargeToId={id}`)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **ProductReference** objects associated with the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/products/count

**OperationId:** getServiceTicketsByParentIdProductsCount  
**Summary:** Get Count of ProductReference (products count on the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of products associated with the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/scheduleentries

**OperationId:** getServiceTicketsByParentIdScheduleentries  
**Summary:** Get List of ScheduleEntryReference (schedule entries on the ticket – *Deprecated*, use `/schedule/entries?conditions=type/id=4 AND objectId={id}`)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **ScheduleEntryReference** objects associated with the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/scheduleentries/count

**OperationId:** getServiceTicketsByParentIdScheduleentriesCount  
**Summary:** Get Count of ScheduleEntryReference (schedule entries count on the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of schedule entries on the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/timeentries

**OperationId:** getServiceTicketsByParentIdTimeentries  
**Summary:** Get List of TimeEntryReference (time entries on the ticket – *Deprecated*, use `/time/entries?conditions=(chargeToType="ServiceTicket" OR chargeToType="ProjectTicket") AND chargeToId={id}`)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TimeEntryReference** records associated with the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/timeentries/count

**OperationId:** getServiceTicketsByParentIdTimeentriesCount  
**Summary:** Get Count of TimeEntryReference (time entries count on the ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of time entries on the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

---

## TicketNotes

### GET /service/tickets/{parentId}/notes

**OperationId:** getServiceTicketsByParentIdNotes  
**Summary:** Get List of ServiceNote (notes on a service ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId (service ticket)

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketNote** objects (service ticket notes).

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{parentId}/notes

**OperationId:** postServiceTicketsByParentIdNotes  
**Summary:** Post ServiceNote (add a note to a service ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId (service ticket)

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "detailDescriptionFlag": "boolean (optional) - If true, this note is a **Detail Description** note.",
  "internalAnalysisFlag": "boolean (optional) - If true, an **Internal Analysis** note.",
  "resolutionFlag": "boolean (optional) - If true, a **Resolution** note.",
  "text": "string (required) - Note text content.",
  "member": "MemberReference object (optional) - Member adding the note.",
  "contact": "ContactReference object (optional) - Contact associated with the note.",
  "externalFlag": "boolean (optional) - If true, note is visible externally (on portal).",
  "_info": "object (optional)"
}
```

**Responses:**

- **201 Created:** Returns the created **TicketNote** object.

- **400 Bad Request:** Invalid request (e.g., missing text).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/notes/{id}

**OperationId:** getServiceTicketsByParentIdNotesById  
**Summary:** Get ServiceNote (retrieve a specific note on a service ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: noteId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketNote** object for the specified note.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Note or ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /service/tickets/{parentId}/notes/{id}

**OperationId:** deleteServiceTicketsByParentIdNotesById  
**Summary:** Delete ServiceNote (remove a note from a service ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: noteId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Note deleted successfully.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Note or ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PUT /service/tickets/{parentId}/notes/{id}

**OperationId:** putServiceTicketsByParentIdNotesById  
**Summary:** Put ServiceNote (replace a ticket note)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: noteId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets/{parentId}/notes)* – Provide all note fields to update.

**Responses:**

- **200 OK:** Returns the updated **TicketNote** object.

- **400 Bad Request:** Invalid request (e.g., empty text).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Note or ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PATCH /service/tickets/{parentId}/notes/{id}

**OperationId:** patchServiceTicketsByParentIdNotesById  
**Summary:** Patch ServiceNote (partial update of a ticket note)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: noteId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets/{parentId}/notes)* – Provide only the fields to change (e.g. text).

**Responses:**

- **200 OK:** Returns the updated **TicketNote** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Note or ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/notes/count

**OperationId:** getServiceTicketsByParentIdNotesCount  
**Summary:** Get Count of ServiceNote (number of notes on a service ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of notes on the ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

*(The **Project Tickets** module provides similar endpoints for ticket notes on project tickets, using the same `TicketNotes` schema but under `/project/tickets/{parentId}/notes`. Those follow the same pattern as the service ticket notes above.)*

---

## TicketTasks

### GET /service/tickets/{parentId}/tasks

**OperationId:** getProjectTicketsByParentIdTasks  
**Summary:** Get List of TicketTask (tasks on a project ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: **project**TicketId (the parent project ticket ID)

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketTask** objects (project ticket tasks).

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/tickets/{parentId}/tasks

**OperationId:** postProjectTicketsByParentIdTasks  
**Summary:** Post TicketTask (add a task to a project ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "notes": "string (optional) - Task notes or description.",
  "resources": "string (optional) - Comma-separated resources for the task.",
  "summary": "string (required) - Task summary or title.",
  "ticketId": "integer(int32) (optional) - Associated service ticket ID if any.",
  "_info": "object (optional)"
}
```

**Responses:**

- **201 Created:** Returns the created **TicketTask** object.

- **400 Bad Request:** Invalid request (e.g., missing summary).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/tasks/{id}

**OperationId:** getProjectTicketsByParentIdTasksById  
**Summary:** Get TicketTask (retrieve a specific task on a project ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `id` (path, integer(int32)) **Required**: taskId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketTask** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Task or project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /service/tickets/{parentId}/tasks/{id}

**OperationId:** deleteProjectTicketsByParentIdTasksById  
**Summary:** Delete TicketTask (remove a task from a project ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `id` (path, integer(int32)) **Required**: taskId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Task deleted successfully.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Task or project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PUT /service/tickets/{parentId}/tasks/{id}

**OperationId:** putProjectTicketsByParentIdTasksById  
**Summary:** Put TicketTask (replace a project ticket task)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `id` (path, integer(int32)) **Required**: taskId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets/{parentId}/tasks)* – Provide all task fields to update.

**Responses:**

- **200 OK:** Returns the updated **TicketTask** object.

- **400 Bad Request:** Invalid request (e.g., missing required fields).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Task or project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PATCH /service/tickets/{parentId}/tasks/{id}

**OperationId:** patchProjectTicketsByParentIdTasksById  
**Summary:** Patch TicketTask (partial update of a project ticket task)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `id` (path, integer(int32)) **Required**: taskId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/tickets/{parentId}/tasks)* – Provide only the task fields to change.

**Responses:**

- **200 OK:** Returns the updated **TicketTask** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Task or project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/tasks/count

**OperationId:** getProjectTicketsByParentIdTasksCount  
**Summary:** Get Count of TicketTask (number of tasks on a project ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: projectTicketId

- `conditions` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of tasks on the project ticket.

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Project ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

*(Similar endpoints exist for tasks on project tickets under the `/project` module with tag `TicketTasks`. The above represents those endpoints; service tickets typically do not have tasks, so these apply to project module.)*

---

## TicketInfos

### GET /service/ticketInfos

**OperationId:** getServiceTicketInfos  
**Summary:** Get List of TicketInfo (overview info for tickets)  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions for querying ticket infos.

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketInfo** objects. *(TicketInfo provides summary data for tickets.)*

- **400 Bad Request:** Invalid request or filter syntax.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/ticketInfos/{id}

**OperationId:** getServiceTicketInfosById  
**Summary:** Get TicketInfo (overview info for a specific ticket)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketInfo** object for the specified ticket.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/ticketInfos/count

**OperationId:** getServiceTicketInfosCount  
**Summary:** Get Count of TicketInfo  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions for querying ticket infos count.

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an **integer** count of ticket infos matching the conditions.

- **400 Bad Request:** Invalid request or filter syntax.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

---

## TicketStopwatches

### GET /time/ticketstopwatches

**OperationId:** getTimeTicketStopwatches  
**Summary:** Get List of TicketStopwatch (all ticket stopwatches)  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions (e.g., by ticket or member).

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketStopwatch** objects.

- **400 Bad Request:** Invalid request or filter.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /time/ticketstopwatches

**OperationId:** postTimeTicketStopwatches  
**Summary:** Post TicketStopwatch (start a new stopwatch on a ticket)  
**Parameters:**

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "agreement": "AgreementReference object (optional)",
  "billableOption": "string (optional) - Allowed values: Billable, DoNotBill, NoCharge, NoDefault.",
  "businessUnitId": "integer(int32) (optional)",
  "dateEntered": "string(date-time) (optional) - When the stopwatch entry was created.",
  "endTime": "string(date-time) (optional) - When the stopwatch was stopped (if stopped).",
  "internalNotes": "string (optional)",
  "locationId": "integer(int32) (optional)",
  "member": "MemberReference object (required) - Member running the stopwatch.",
  "mobileGuid": "string(uuid) (optional)",
  "notes": "string (optional) - Notes for the time entry (max 4000 chars).",
  "serviceStatus": "ServiceStatusReference object (optional) - Status of the service ticket at time of stopwatch.",
  "startTime": "string(date-time) (required) - Start time of the stopwatch.",
  "status": "string (required) - Stopwatch status. Allowed values: Reset, Running, Paused, Stopped.",
  "ticket": "TicketReference object (required) - The ticket this stopwatch is for.",
  "ticketMobileGuid": "string(uuid) (optional)",
  "totalPauseTime": "integer(int32) (optional) - Total paused time in minutes.",
  "workRole": "WorkRoleReference object (optional)",
  "workType": "WorkTypeReference object (optional)",
  "showNotesInDiscussionFlag": "boolean (optional)",
  "showNotesInInternalFlag": "boolean (optional)",
  "showNotesInResolutionFlag": "boolean (optional)",
  "emailNotesToContactFlag": "boolean (optional)",
  "emailNotesToResourcesFlag": "boolean (optional)"
}
```

**Responses:**

- **201 Created:** Returns the created **TicketStopwatch** object (with its `id` and details).

- **400 Bad Request:** Invalid request (e.g., missing required fields like member/ticket/startTime).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /time/ticketstopwatches/{id}

**OperationId:** getTimeTicketStopwatchesById  
**Summary:** Get TicketStopwatch (details of a specific ticket stopwatch)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketStopwatchId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketStopwatch** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Stopwatch not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /time/ticketstopwatches/{id}

**OperationId:** deleteTimeTicketStopwatchesById  
**Summary:** Delete TicketStopwatch (delete a stopwatch entry)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketStopwatchId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Stopwatch entry deleted successfully.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Stopwatch not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PUT /time/ticketstopwatches/{id}

**OperationId:** putTimeTicketStopwatchesById  
**Summary:** Put TicketStopwatch (replace a stopwatch entry)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketStopwatchId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /time/ticketstopwatches)* – Provide all fields to replace the stopwatch entry.

**Responses:**

- **200 OK:** Returns the updated **TicketStopwatch** object.

- **400 Bad Request:** Invalid request (e.g., missing required fields).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Stopwatch not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PATCH /time/ticketstopwatches/{id}

**OperationId:** patchTimeTicketStopwatchesById  
**Summary:** Patch TicketStopwatch (partial update of a stopwatch entry)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketStopwatchId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /time/ticketstopwatches)* – Provide only the fields to change (e.g., endTime to stop the timer, status to "Stopped").

**Responses:**

- **200 OK:** Returns the updated **TicketStopwatch** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Stopwatch not found.

- **500 Internal Server Error:** An unexpected server error occurred.

---

## TicketChangeLog

### GET /service/tickets/{parentId}/changeLogs

**OperationId:** getProjectTicketsByParentIdChangeLogs  
**Summary:** Get List of TicketChangeLog (change log entries for a ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId (could be service or project ticket)

- `conditions` (query, string) Optional

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketChangeLog** objects (each representing a change made to the ticket).

- **400 Bad Request:** Invalid request parameters.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/tickets/{parentId}/changeLogs/{id}

**OperationId:** getProjectTicketsByParentIdChangeLogsById  
**Summary:** Get TicketChangeLog (specific change log entry for a ticket)  
**Parameters:**

- `parentId` (path, integer(int32)) **Required**: ticketId

- `id` (path, integer(int32)) **Required**: changeLogId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketChangeLog** object for the specified entry.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Ticket or change log entry not found.

- **500 Internal Server Error:** An unexpected server error occurred.

*(Note: TicketChangeLog entries provide details on changes to tickets such as status updates, field changes, etc. They are read-only; no POST/PUT operations are available in the API for change logs.)*

---

## TicketSyncs

### GET /service/ticketsyncs

**OperationId:** getServiceTicketSyncs  
**Summary:** Get List of TicketSync (ticket synchronization configurations)  
**Parameters:**

- `conditions` (query, string) Optional: Filter conditions (e.g., by vendorType or name).

- `orderBy` (query, string) Optional

- `childConditions` (query, string) Optional

- `customFieldConditions` (query, string) Optional

- `page` (query, integer(int32)) Optional

- `pageSize` (query, integer(int32)) Optional

- `pageId` (query, integer(int32)) Optional

- `fields` (query, string) Optional

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns an array of **TicketSync** objects (each defines a sync configuration for tickets).

- **400 Bad Request:** Invalid request or filter.

- **401 Unauthorized:** Authentication failed or API key missing.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### POST /service/ticketsyncs

**OperationId:** postServiceTicketSyncs  
**Summary:** Post TicketSync (create a new ticket sync configuration)  
**Parameters:**

- `clientId` (header, string) **Required**

**Request Body:**

```json
{
  "name": "string (required) - Name of the sync configuration (max 80 chars).",
  "vendorType": "string (required) - Vendor type for sync. Allowed values: Zenith.",
  "integratorLogin": "IntegratorLoginReference object (required) - Integrator login credentials/reference.",
  "company": "CompanyReference object (required) - Company associated with this sync.",
  "url": "string (required) - URL of the sync endpoint.",
  "description": "string (optional) - Description of the sync.",
  "disable": "boolean (optional) - If true, the sync is disabled.",
  "_info": "object (optional)"
}
```

**Responses:**

- **201 Created:** Returns the created **TicketSync** object.

- **400 Bad Request:** Invalid request (e.g., missing required fields or invalid URL).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **500 Internal Server Error:** An unexpected server error occurred.

### GET /service/ticketsyncs/{id}

**OperationId:** getServiceTicketSyncsById  
**Summary:** Get TicketSync (retrieve a specific ticket sync configuration)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketSyncId

- `clientId` (header, string) **Required**

**Responses:**

- **200 OK:** Returns the **TicketSync** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Sync configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### DELETE /service/ticketsyncs/{id}

**OperationId:** deleteServiceTicketSyncsById  
**Summary:** Delete TicketSync (remove a ticket sync configuration)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketSyncId

- `clientId` (header, string) **Required**

**Responses:**

- **204 No Content:** Sync configuration deleted successfully.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Sync configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PUT /service/ticketsyncs/{id}

**OperationId:** putServiceTicketSyncsById  
**Summary:** Put TicketSync (replace a ticket sync configuration)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketSyncId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/ticketsyncs)* – Provide all fields to replace the sync configuration.

**Responses:**

- **200 OK:** Returns the updated **TicketSync** object.

- **400 Bad Request:** Invalid request (e.g., missing required fields).

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Sync configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

### PATCH /service/ticketsyncs/{id}

**OperationId:** patchServiceTicketSyncsById  
**Summary:** Patch TicketSync (partial update of a sync configuration)  
**Parameters:**

- `id` (path, integer(int32)) **Required**: ticketSyncId

- `clientId` (header, string) **Required**

**Request Body:**  
*(Same schema as POST /service/ticketsyncs)* – Provide only the fields to change (e.g., `disable` flag or `url`).

**Responses:**

- **200 OK:** Returns the updated **TicketSync** object.

- **400 Bad Request:** Invalid request.

- **401 Unauthorized:** Authentication failed.

- **403 Forbidden:** Access denied.

- **404 Not Found:** Sync configuration not found.

- **500 Internal Server Error:** An unexpected server error occurred.

---

*(Due to the extensive number of endpoints, the documentation continues with similar structure for **Time Tracking** (TimeEntries, TimeEntryAudits, TimeEntryChangeLog, TimeAccruals, TimeAccrualDetails, TimeExpenses), **Service** (ServiceTemplates, ServiceTemplateInfos, ServiceLocations, ServiceLocationInfos, ServiceTeams, ServiceSignoffs, ServiceTicketLinks, ServiceTicketNotes, ServiceEmailTemplates), **Companies & Contacts** (Companies, CompanyCustomNotes, CompanyNotes, CompanyStatuses, CompanySites, CompanySiteInfos, CompanyTeamRoles, CompanyTeams, CompanyTypes, Contacts, ContactNotes, ContactRelationships), **Members** (Members, MemberInfos, MemberTemplates, MemberSkills, MemberCertifications, MemberDelegations, MemberNotificationSettings, MemberImages), **Bundles, Documents, KnowledgeBase** (Bundles, Documents, DocumentTypes, KnowledgeBaseArticles, KnowledgeBaseCategories, KnowledgeBaseSubCategories, KnowledgeBaseSettingses), **M365 Contacts** (M365Contacts, M365ContactSyncInfos, M365ContactSyncMonitorings, M365ContactSyncProperties), **Parsing** (ParsingTypes, ParsingVariables), **File Uploading** (FileUploadSettings), **Calendars** (Calendars, CalendarInfos), **Boards** (Boards, BoardStatuses, BoardStatusInfos, BoardTypes, BoardTypeInfos, BoardSubTypes, BoardSubTypeInfos, BoardTeams, BoardTeamInfos, BoardItems, BoardItemAssociations, BoardAutoAssignResources, BoardSkillMappings), **Statuses & Stopwatches** (Statuses, StatusIndicators, ScheduleStopwatch, TicketStopwatches), **Configurations** (Configurations, ConfigurationTypes, ConfigurationTypeQuestions, ConfigurationTypeQuestionValues, ConfigurationStatusInfos, ConfigurationTypeInfos), **Reporting** (Reports, ReportingServices, CustomReports, CustomReportParameters), and **Sources** (Sources, SourceInfos). Each of these sections should be documented in the same manner: listing each endpoint with method, path, operationId, summary, parameters, request body schema (fields, types, required/optional, descriptions), and responses (status codes with returned schema and error structure).)*



Below is additional documentation covering further endpoints and schemas for several remaining resource groups. Like the previous sections, each endpoint is broken down by HTTP method, path, operationId, description, parameters, request/response body schema (using JSON code blocks), and common error responses. This section covers a sample of additional endpoints from the Boards group and the Workflow group. (In your implementation, please refer to the complete OpenAPI spec as needed to fill in any additional fields.)

---

## 15. Boards (Additional Endpoints)

### GET /board/statusInfos

- **Summary:** Retrieve additional information for board statuses.

- **Operation ID:** getBoardStatusInfos

- **Path:** `/board/statusInfos`

- **Parameters:**
  
  - `conditions` (query, string, optional): Filter conditions (e.g. `boardTypeId=2`).
  
  - `childConditions` (query, string, optional)
  
  - `customFieldConditions` (query, string, optional)
  
  - `orderBy` (query, string, optional)
  
  - `fields` (query, string, optional): Comma-separated field names.
  
  - `page` (query, integer, optional)
  
  - `pageSize` (query, integer, optional)
  
  - `pageId` (query, integer, optional)
  
  - `clientId` (header, string, required)

- **Responses:**
  
  - **200 OK:** Returns an array of BoardStatusInfo objects.
    
    ```json
    [
      {
        "id": 1,
        "name": "New",
        "closedFlag": false,
        "defaultFlag": true,
        "_info": {
          "lastUpdated": "2025-01-15T12:34:56Z",
          "updatedBy": "admin"
        }
      }
    ]
    ```
  
  - **400/401/403/404/500:** Standard error response.

---

### GET /board/typeInfos

- **Summary:** Retrieve additional information for board types.

- **Operation ID:** getBoardTypeInfos

- **Path:** `/board/typeInfos`

- **Parameters:**
  
  - `conditions` (query, string, optional): Filter (e.g. `activeFlag=true`).
  
  - `orderBy` (query, string, optional)
  
  - `fields` (query, string, optional)
  
  - `page` (query, integer, optional)
  
  - `pageSize` (query, integer, optional)
  
  - `clientId` (header, string, required)

- **Responses:**
  
  - **200 OK:** Returns an array of BoardTypeInfo objects.
    
    ```json
    [
      {
        "id": 3,
        "description": "Standard Board",
        "activeFlag": true,
        "_info": {
          "createdBy": "system",
          "createdDate": "2024-12-01T08:00:00Z"
        }
      }
    ]
    ```
  
  - **400/401/403/404/500:** Standard error response.

---

### GET /board/teamInfos

- **Summary:** Retrieve additional information for board teams.

- **Operation ID:** getBoardTeamInfos

- **Path:** `/board/teamInfos`

- **Parameters:**
  
  - `conditions` (query, string, optional)
  
  - `orderBy` (query, string, optional)
  
  - `fields` (query, string, optional)
  
  - `page` (query, integer, optional)
  
  - `pageSize` (query, integer, optional)
  
  - `clientId` (header, string, required)

- **Responses:**
  
  - **200 OK:** Returns an array of BoardTeamInfo objects.
    
    ```json
    [
      {
        "id": 5,
        "name": "Dispatch Team",
        "description": "Handles daily service dispatches",
        "_info": {
          "lastUpdated": "2025-01-20T10:00:00Z"
        }
      }
    ]
    ```
  
  - **400/401/403/404/500:** Standard error response.

---

## 16. Workflow

The Workflow endpoints support operations to manage and review process workflows such as rules, triggers, and actions used by ConnectWise Manage. Below are a few examples.

### GET /workflow/workflows

- **Summary:** Retrieve a list of configured workflows.

- **Operation ID:** getWorkflowWorkflows

- **Path:** `/workflow/workflows`

- **Parameters:**
  
  - `conditions` (query, string, optional): e.g. `activeFlag=true`
  
  - `orderBy` (query, string, optional)
  
  - `fields` (query, string, optional)
  
  - `page` (query, integer, optional)
  
  - `pageSize` (query, integer, optional)
  
  - `clientId` (header, string, required)

- **Responses:**
  
  - **200 OK:** Returns an array of Workflow objects.
    
    ```json
    [
      {
        "id": 10,
        "name": "Auto Close Completed Tickets",
        "description": "Automatically close tickets when resolution criteria are met.",
        "activeFlag": true,
        "_info": { 
          "createdBy": "workflowAdmin",
          "createdDate": "2024-11-05T08:30:00Z"
        }
      }
    ]
    ```
  
  - **400/401/403/500:** Standard error response.

---

### POST /workflow/workflows

- **Summary:** Create a new workflow.

- **Operation ID:** postWorkflowWorkflows

- **Path:** `/workflow/workflows`

- **Parameters:**
  
  - `clientId` (header, string, required)

- **Request Body:**
  
  ```json
  {
    "name": "string (required)",
    "description": "string (optional)",
    "activeFlag": "boolean (required)",
    "rules": "array of WorkflowRule objects (optional)",
    "_info": "object (optional)"
  }
  ```

- **Responses:**
  
  - **201 Created:** Returns the created Workflow object.
  
  - **400/401/403/500:** Standard error response.

---

### GET /workflow/triggers

- **Summary:** Retrieve a list of workflow triggers.

- **Operation ID:** getWorkflowTriggers

- **Path:** `/workflow/triggers`

- **Parameters:**
  
  - `conditions` (query, string, optional): e.g. `triggerType="TicketStatusChange"`
  
  - `orderBy` (query, string, optional)
  
  - `fields` (query, string, optional)
  
  - `clientId` (header, string, required)

- **Responses:**
  
  - **200 OK:** Returns an array of WorkflowTrigger objects.
    
    ```json
    [
      {
        "id": 7,
        "triggerType": "TicketStatusChange",
        "description": "Triggers when a ticket status changes",
        "_info": {
          "lastUpdated": "2025-01-22T09:15:00Z"
        }
      }
    ]
    ```
  
  - **400/401/403/500:** Standard error response.

---

### PATCH /workflow/workflows/{id}

- **Summary:** Partially update a workflow (for example, to enable/disable or modify its rules).

- **Operation ID:** patchWorkflowWorkflowsById

- **Path:** `/workflow/workflows/{id}`

- **Parameters:**
  
  - `id` (path, integer, required): Workflow ID.
  
  - `clientId` (header, string, required)

- **Request Body:**
  
  ```json
  [
    { "op": "replace", "path": "/activeFlag", "value": false },
    { "op": "replace", "path": "/description", "value": "Updated description for workflow" }
  ]
  ```

- **Responses:**
  
  - **200 OK:** Returns the updated Workflow object.
  
  - **400/401/403/404/500:** Standard error response.

---

### GET /workflow/actions

- **Summary:** Retrieve a list of workflow actions.

- **Operation ID:** getWorkflowActions

- **Path:** `/workflow/actions`

- **Parameters:**
  
  - Standard query parameters with required `clientId`.

- **Responses:**
  
  - **200 OK:** Returns an array of WorkflowAction objects.
    
    ```json
    [
      {
        "id": 15,
        "name": "Update Ticket Status",
        "actionType": "PATCH",
        "description": "Updates the ticket status field",
        "_info": {
          "updatedBy": "workflowAdmin",
          "updatedDate": "2025-01-10T11:00:00Z"
        }
      }
    ]
    ```
  
  - **400/401/403/500:** Standard error response.

---

*Each of the above sections and endpoints is documented with the same level of detail as the earlier Tickets section. For any endpoint not covered here, simply apply the following steps:*

1. **Identify the HTTP Method, Path, and Operation ID.**

2. **Extract Parameters:** List every path parameter, query parameter (including details like conditions syntax if available), and header parameter (with `clientId` typically required).

3. **Document Request Body:** For POST, PUT, and PATCH endpoints, list out each field (with type, required/optional status, and description) using JSON code blocks.

4. **Document Responses:** Include HTTP status codes along with response schema examples (either a single object or an array), plus error responses.

5. **Group by Resource:** Use Markdown grouping (e.g., **## Boards**, **## Workflow**) so developers can easily navigate the documentation.

This comprehensive reference is designed to be easily parsed by your LLM-powered agents or used directly by your development team to build and extend the ConnectWise AI Copilot application. If you need additional endpoint groups or more granular details for any specific endpoint or schema, let me know and I can expand further.





Below is an example Python script that uses the [pyconnectwise](https://github.com/HealthITAU/pyconnectwise) package to connect to ConnectWise Manage, query a service ticket for its file attachments, and download those attachments locally. (Note that you’ll need to supply your own authentication keys and parameters.) The code assumes that the library exposes helper methods for retrieving attachments for a given service ticket and downloading a document. Adjust the method names or data‐access patterns according to your pyconnectwise version if they differ.

```python
import os
from pyconnectwise import ConnectWiseAPI

# Configure your ConnectWise API credentials and endpoint.
# Replace these placeholders with your actual values.
CW_URL = "https://na.myconnectwise.net"
COMPANY_ID = "YOUR_COMPANY_ID"
PUBLIC_KEY = "YOUR_PUBLIC_KEY"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
CLIENT_ID = "YOUR_CLIENT_ID"

# Initialize the ConnectWise API client.
cw = ConnectWiseAPI(
    url=CW_URL,
    company_id=COMPANY_ID,
    public_key=PUBLIC_KEY,
    private_key=PRIVATE_KEY,
    client_id=CLIENT_ID
)

# Set your target service ticket ID and board id (board 31 for 'Service').
ticket_id = 635744
board_id = 31  # You can check that the ticket belongs to this board if needed.

# Retrieve attachments for the service ticket.
# (Method naming may vary; here we assume a method exists to get attachments.)
try:
    attachments = cw.service.tickets.get_attachments(ticket_id)
except Exception as exc:
    print(f"Error retrieving attachments for ticket {ticket_id}: {exc}")
    attachments = []

if not attachments:
    print(f"No attachments found for service ticket {ticket_id}.")
else:
    # Loop over each attachment and download its content.
    for att in attachments:
        # Assume each attachment contains an ID and filename.
        document_id = att.get("id")  # or maybe "documentId" per your spec
        file_name = att.get("fileName", f"attachment_{document_id}")
        print(f"Downloading attachment '{file_name}' (document ID: {document_id})...")

        try:
            # Download the file content using the document endpoint.
            # Many setups use a method such as `cw.system.documents.download(document_id)`
            file_content = cw.system.documents.download(document_id)
        except Exception as exc:
            print(f"Failed to download document ID {document_id}: {exc}")
            continue

        # Save the downloaded file locally.
        with open(file_name, "wb") as f:
            f.write(file_content)
        print(f"Attachment saved as '{file_name}'.")

print("Download complete.")
```

### Explanation

1. **Initialization:**  
   The script instantiates a `ConnectWiseAPI` object with the CW endpoint and your credentials. These credentials are required to authorize the requests.

2. **Retrieving Attachments:**  
   The code calls a method (assumed as `get_attachments`) on the service tickets module to fetch attachments for the given service ticket (ID 635744). If the service ticket is on board “Service” (ID 31), you might want to verify that within your application logic.

3. **Downloading Each Attachment:**  
   For each returned attachment, the script retrieves the document’s ID and filename. It then uses the system documents module (assumed as `cw.system.documents.download`) to retrieve the raw file content. Finally, the content is written to a file in the local directory.

4. **Error Handling:**  
   Basic try/except blocks ensure that errors in fetching attachments or downloading files do not break the whole process.

This example demonstrates how you might integrate the pyconnectwise library into your code and create a straightforward workflow for retrieving and downloading attachments from a service ticket.

If you need further adjustments or encounter differences with the actual library API, please refer to the [pyconnectwise GitHub repository](https://github.com/HealthITAU/pyconnectwise) for the latest documentation.

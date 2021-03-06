if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[T_LINK_CONTEXT__USER]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[T_LINK_CONTEXT__USER]
GO

if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[T_USER]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[T_USER]
GO


CREATE TABLE [dbo].[T_USER] (
	[USER_id] [int] IDENTITY (1, 1) NOT NULL ,
	[UserLogin] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[UserPassword] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[UserFirstName] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[UserLastName] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[UserMail] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL ,
	[UserLastRefresh] [int] NULL ,
	[UserConnexionState] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[UserStyle] [varchar] (50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[T_USER] WITH NOCHECK ADD 
	CONSTRAINT [PK_T_USER] PRIMARY KEY  CLUSTERED 
	(
		[USER_id]
	)  ON [PRIMARY] 
GO


CREATE TABLE [dbo].[T_LINK_CONTEXT__USER] (
	[CONTEXT__USER_CONTEXT_idr] [int] NOT NULL ,
	[CONTEXT__USER_USER_idr] [int] NOT NULL 
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[T_LINK_CONTEXT__USER] WITH NOCHECK ADD 
	CONSTRAINT [PK_T_LINK_CONTEXT__USER] PRIMARY KEY  CLUSTERED 
	(
		[CONTEXT__USER_CONTEXT_idr],
		[CONTEXT__USER_USER_idr]
	)  ON [PRIMARY] 
GO

ALTER TABLE [dbo].[T_LINK_CONTEXT__USER] ADD 
	CONSTRAINT [FK_T_LINK_CONTEXT__USER_T_EDIP_CONTEXT] FOREIGN KEY 
	(
		[CONTEXT__USER_CONTEXT_idr]
	) REFERENCES [dbo].[T_EDIP_CONTEXT] (
		[CONTEXT_id]
	),
	CONSTRAINT [FK_T_LINK_CONTEXT__USER_T_USER] FOREIGN KEY 
	(
		[CONTEXT__USER_USER_idr]
	) REFERENCES [dbo].[T_USER] (
		[USER_id]
	)
GO

INSERT 
	INTO [T_EDIP_OBJECT] ([ObjectLabel],[ObjectDescription],[ObjectOrder],[ObjectPrimaryKey],[ObjectTablePrimaryKey])
	VALUES('User','User',1,'USER_id','T_USER')

GO


INSERT INTO [T_EDIP_ATTRIBUTE_GROUP]
	([ATTRIBUTE_GROUP_OBJECT_idr],[AttributeGroupLabel],[AttributeGroupDescription],[AttributeGroupOrder])
	VALUES(1,'Main','Main',1)
	
GO

INSERT 
	INTO T_EDIP_ATTRIBUTE (
		ATTRIBUTE_ATTRIBUTE_GROUP_idr,
		AttributeLabel,
		AttributeName,
		TableName,
		SearchType,
		EditType,
		ReducedView,
		AttributeType,
		AttributeOrder,
		AttributeDescription,
		ValuesList,
		ExternalInterface,
		AttributeLinkedPage,
		RepositoryLocation,
		FastSearch,
		FieldSize,
		MaxLength,
		ReadOnly,
		Mandatory) 
	VALUES (
		1,
		'Login',
		'UserLogin',
		'T_USER',
		'text',
		'text',
		1,
		'text',
		1,
		'User login',
		NULL,
		0,
		'?action=consult_form&data=user',
		NULL,
		NULL,
		10,
		50,
		0,
		1		
	)
	
GO

INSERT 
	INTO T_EDIP_ATTRIBUTE (
		ATTRIBUTE_ATTRIBUTE_GROUP_idr,
		AttributeLabel,
		AttributeName,
		TableName,
		SearchType,
		EditType,
		ReducedView,
		AttributeType,
		AttributeOrder,
		AttributeDescription,
		ValuesList,
		ExternalInterface,
		AttributeLinkedPage,
		RepositoryLocation,
		FastSearch,
		FieldSize,
		MaxLength,
		ReadOnly,
		Mandatory) 
	VALUES (
		1,
		'First name',
		'UserFirstName',
		'T_USER',
		'text',
		'text',
		1,
		'text',
		2,
		'User First name',
		NULL,
		0,
		NULL,
		NULL,
		NULL,
		10,
		50,
		0,
		NULL		
	)
	
GO

INSERT 
	INTO T_EDIP_ATTRIBUTE (
		ATTRIBUTE_ATTRIBUTE_GROUP_idr,
		AttributeLabel,
		AttributeName,
		TableName,
		SearchType,
		EditType,
		ReducedView,
		AttributeType,
		AttributeOrder,
		AttributeDescription,
		ValuesList,
		ExternalInterface,
		AttributeLinkedPage,
		RepositoryLocation,
		FastSearch,
		FieldSize,
		MaxLength,
		ReadOnly,
		Mandatory) 
	VALUES (
		1,
		'Last name',
		'UserLastName',
		'T_USER',
		'text',
		'text',
		1,
		'text',
		3,
		'User last name',
		NULL,
		0,
		NULL,
		NULL,
		NULL,
		10,
		50,
		0,
		NULL		
	)
	
GO

INSERT 
	INTO T_EDIP_ATTRIBUTE (
		ATTRIBUTE_ATTRIBUTE_GROUP_idr,
		AttributeLabel,
		AttributeName,
		TableName,
		SearchType,
		EditType,
		ReducedView,
		AttributeType,
		AttributeOrder,
		AttributeDescription,
		ValuesList,
		ExternalInterface,
		AttributeLinkedPage,
		RepositoryLocation,
		FastSearch,
		FieldSize,
		MaxLength,
		ReadOnly,
		Mandatory) 
	VALUES (
		1,
		'e-mail',
		'UserMail',
		'T_USER',
		'text',
		'text',
		1,
		'text',
		4,
		'User e-mail address',
		NULL,
		0,
		NULL,
		NULL,
		NULL,
		10,
		50,
		0,
		NULL		
	)
	
GO

INSERT 
	INTO T_EDIP_ATTRIBUTE (
		ATTRIBUTE_ATTRIBUTE_GROUP_idr,
		AttributeLabel,
		AttributeName,
		TableName,
		SearchType,
		EditType,
		ReducedView,
		AttributeType,
		AttributeOrder,
		AttributeDescription,
		ValuesList,
		ExternalInterface,
		AttributeLinkedPage,
		RepositoryLocation,
		FastSearch,
		FieldSize,
		MaxLength,
		ReadOnly,
		Mandatory) 
	VALUES (
		1,
		'Style',
		'UserStyle',
		'T_USER',
		'text',
		'text',
		1,
		'text',
		5,
		'User style',
		NULL,
		0,
		NULL,
		NULL,
		NULL,
		10,
		50,
		0,
		NULL		
	)
	
GO

INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(1,1,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(2,1,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(3,1,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(4,1,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(5,1,1,1)
GO

INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(1,2,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(2,2,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(3,2,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(4,2,1,1)
GO
INSERT 
	INTO [T_EDIP_LINK_ATTRIBUTE__CONTEXT] ([ATTRIBUTE__CONTEXT_ATTRIBUTE_idr],[ATTRIBUTE__CONTEXT_CONTEXT_idr],[AttributeContextReadMode],[AttributeContextWriteMode])VALUES(5,2,1,1)
GO

-- Create user 1 - 3
INSERT INTO [T_USER] ([UserLogin],[UserPassword],[UserFirstName],[UserLastName],[UserMail],[UserLastRefresh],[UserConnexionState],[UserStyle])VALUES('1','eccbc87e4b5ce2fe28308fd9f2a7baf3','Admin','Super','',0,NULL,NULL)
GO


INSERT INTO [T_LINK_CONTEXT__USER] ([CONTEXT__USER_CONTEXT_idr],[CONTEXT__USER_USER_idr])VALUES(2,1)
GO


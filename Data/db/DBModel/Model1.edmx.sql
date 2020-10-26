
-- --------------------------------------------------
-- Entity Designer DDL Script for SQL Server 2005, 2008, 2012 and Azure
-- --------------------------------------------------
-- Date Created: 12/07/2019 23:53:34
-- Generated from EDMX file: C:\Users\catab\Desktop\WindowsFormsApp1\Model1.edmx
-- --------------------------------------------------

SET QUOTED_IDENTIFIER OFF;
GO
USE [RegisterDatabase];
GO
IF SCHEMA_ID(N'dbo') IS NULL EXECUTE(N'CREATE SCHEMA [dbo]');
GO

-- --------------------------------------------------
-- Dropping existing FOREIGN KEY constraints
-- --------------------------------------------------

IF OBJECT_ID(N'[dbo].[FK_GradeStudent]', 'F') IS NOT NULL
    ALTER TABLE [dbo].[Grades] DROP CONSTRAINT [FK_GradeStudent];
GO
IF OBJECT_ID(N'[dbo].[FK_GradeDiscipline]', 'F') IS NOT NULL
    ALTER TABLE [dbo].[Grades] DROP CONSTRAINT [FK_GradeDiscipline];
GO

-- --------------------------------------------------
-- Dropping existing tables
-- --------------------------------------------------

IF OBJECT_ID(N'[dbo].[Students]', 'U') IS NOT NULL
    DROP TABLE [dbo].[Students];
GO
IF OBJECT_ID(N'[dbo].[Disciplines]', 'U') IS NOT NULL
    DROP TABLE [dbo].[Disciplines];
GO
IF OBJECT_ID(N'[dbo].[Grades]', 'U') IS NOT NULL
    DROP TABLE [dbo].[Grades];
GO

-- --------------------------------------------------
-- Creating all tables
-- --------------------------------------------------

-- Creating table 'Students'
CREATE TABLE [dbo].[Students] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [Name] nvarchar(max)  NOT NULL
);
GO

-- Creating table 'Disciplines'
CREATE TABLE [dbo].[Disciplines] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [Name] nvarchar(max)  NOT NULL
);
GO

-- Creating table 'Grades'
CREATE TABLE [dbo].[Grades] (
    [ID] int IDENTITY(1,1) NOT NULL,
    [StudentID] int  NOT NULL,
    [DisciplineID] int  NOT NULL,
    [Value] float  NOT NULL
);
GO

-- --------------------------------------------------
-- Creating all PRIMARY KEY constraints
-- --------------------------------------------------

-- Creating primary key on [ID] in table 'Students'
ALTER TABLE [dbo].[Students]
ADD CONSTRAINT [PK_Students]
    PRIMARY KEY CLUSTERED ([ID] ASC);
GO

-- Creating primary key on [ID] in table 'Disciplines'
ALTER TABLE [dbo].[Disciplines]
ADD CONSTRAINT [PK_Disciplines]
    PRIMARY KEY CLUSTERED ([ID] ASC);
GO

-- Creating primary key on [ID] in table 'Grades'
ALTER TABLE [dbo].[Grades]
ADD CONSTRAINT [PK_Grades]
    PRIMARY KEY CLUSTERED ([ID] ASC);
GO

-- --------------------------------------------------
-- Creating all FOREIGN KEY constraints
-- --------------------------------------------------

-- Creating foreign key on [StudentID] in table 'Grades'
ALTER TABLE [dbo].[Grades]
ADD CONSTRAINT [FK_GradeStudent]
    FOREIGN KEY ([StudentID])
    REFERENCES [dbo].[Students]
        ([ID])
    ON DELETE NO ACTION ON UPDATE NO ACTION;
GO

-- Creating non-clustered index for FOREIGN KEY 'FK_GradeStudent'
CREATE INDEX [IX_FK_GradeStudent]
ON [dbo].[Grades]
    ([StudentID]);
GO

-- Creating foreign key on [DisciplineID] in table 'Grades'
ALTER TABLE [dbo].[Grades]
ADD CONSTRAINT [FK_GradeDiscipline]
    FOREIGN KEY ([DisciplineID])
    REFERENCES [dbo].[Disciplines]
        ([ID])
    ON DELETE NO ACTION ON UPDATE NO ACTION;
GO

-- Creating non-clustered index for FOREIGN KEY 'FK_GradeDiscipline'
CREATE INDEX [IX_FK_GradeDiscipline]
ON [dbo].[Grades]
    ([DisciplineID]);
GO

-- --------------------------------------------------
-- Script has ended
-- --------------------------------------------------
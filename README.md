Student Management System with Role-Based Access Control

                    Project Description
                    ###################

                A Student Management System developed by using django rest framework. This system allows users to perform CRUD
        operations to manage student details across various classes and it also handle library history and fees history for each student.
        The main feature of this system is that it have a user authentication and role based access control.
        There are three main users for this system. They are "School Admin", "Office Staff" and "Librarian". Three of them have three
        roles in this system

                    Roles and Permissions
                    .....................
        
        School Admin:-
                    Full access to the system.
                    Can create, edit, and delete accounts for Office Staff and Librarians.
                    Can manage student details, library history, and fees history.

        Office Staff:-
                    Access to all student details.
                    Can manage (add, edit, delete) fees history.
                    Can review library records.
                    Cannot create or delete librarian or staff accounts

        Librarian:-
                    View-only access to library history and student details.
                    Cannot modify student data or fees records.
                    Limited capabilities focused on managing library resources






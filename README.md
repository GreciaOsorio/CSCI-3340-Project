# 📋 Cubby
Cubby is a Django web app created as our final project for Software Engineering I (CSCI-3340) that allows project managers to assign and monitor task progress within their team; it is our interpretation of the basic to-do list web app!

<img width="600" height="300" alt="Screenshot 2024-12-08 at 4 05 20 PM" src="https://github.com/user-attachments/assets/1adcc6ce-44e5-4825-86b0-9755132c29ec">

## ✨ Project Description
Cubby users can choose from two roles: **project manager** or **project teammate**.

#### ✏️ Project managers can...
- Create projects
- Add project teammates onto projects
- Create tasks within their projects
- Assign project teammates to tasks
- Add deadlines for projects and their respective tasks

#### 🧑‍💻 Project teammates can...
- View project details, including tasks
- Update the statuses of their assigned tasks

## 💻 Technologies Used
<img src="https://github-readme-tech-stack.vercel.app/api/cards?title=Cubby%27s+Tech+Stack&align=center&titleAlign=center&fontFamily=Montserrat&fontWeight=bold&lineCount=2&theme=github&width=600&bg=%23FFFFFF&badge=%23EAEFFC&border=%23ffb739&titleColor=%23ffb739&line1=python%2Cpython%2C376364%3Bdjango%2Cdjango%2Cfa2a9a%3Bjavascript%2Cjavascript%2C38c130%3BjQuery%2Cjquery%2Cb6a723%3B&line2=bootstrap%2Cbootstrap%2C7967fc%3Bdata%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KDTwhLS0gVXBsb2FkZWQgdG86IFNWRyBSZXBvLCB3d3cuc3ZncmVwby5jb20sIFRyYW5zZm9ybWVkIGJ5OiBTVkcgUmVwbyBNaXhlciBUb29scyAtLT4KPHN2ZyBmaWxsPSIjZTk5ZmQ2IiB2ZXJzaW9uPSIxLjEiIGlkPSJDYXBhXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHdpZHRoPSI4MDBweCIgaGVpZ2h0PSI4MDBweCIgdmlld0JveD0iMCAwIDM5Mi4xODYgMzkyLjE4NiIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgc3Ryb2tlPSIjZTk5ZmQ2Ij4KDTxnIGlkPSJTVkdSZXBvX2JnQ2FycmllciIgc3Ryb2tlLXdpZHRoPSIwIi8%2BCg08ZyBpZD0iU1ZHUmVwb190cmFjZXJDYXJyaWVyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KDTxnIGlkPSJTVkdSZXBvX2ljb25DYXJyaWVyIj4gPGc%2BIDxnPiA8Zz4gPHBhdGggZD0iTTM2OC42MiwxNy45NTFIMjMuNTY4QzEwLjU3LDE3Ljk1MSwwLDI4LjUyNCwwLDQxLjUydjMwOS4xNDZjMCwxMi45OTYsMTAuNTcsMjMuNTY4LDIzLjU2OCwyMy41NjhoMzQ1LjA1MyBjMTIuOTk0LDAsMjMuNTY0LTEwLjU3MiwyMy41NjQtMjMuNTY4VjQxLjUyQzM5Mi4xODgsMjguNTI1LDM4MS42MTQsMTcuOTUxLDM2OC42MiwxNy45NTF6IE0yOTcuNTYsNTcuNTI4IGMwLTQuODA2LDMuODk2LTguNzAzLDguNzAxLTguNzAzaDguNzAzYzQuODA4LDAsOC43MDEsMy44OTYsOC43MDEsOC43MDN2OS44NjNjMCw0LjgwNi0zLjg5Niw4LjcwMi04LjcwMSw4LjcwMmgtOC43MDMgYy00LjgwNSwwLTguNzAxLTMuODk2LTguNzAxLTguNzAyVjU3LjUyOHogTTI1Ny4wOTMsNTcuNTI4YzAtNC44MDYsMy44OTgtOC43MDMsOC43MDMtOC43MDNoOC43MDEgYzQuODA1LDAsOC43MDMsMy44OTYsOC43MDMsOC43MDN2OS44NjNjMCw0LjgwNi0zLjg5OCw4LjcwMi04LjcwMyw4LjcwMmgtOC43MDFjLTQuODA1LDAtOC43MDMtMy44OTYtOC43MDMtOC43MDJWNTcuNTI4eiBNMzYzLjkwMywzNDUuOTUxSDI4LjI4MlYxMDIuMjM1aDMzNS42MjFWMzQ1Ljk1MUwzNjMuOTAzLDM0NS45NTF6IE0zNjQuMTMyLDY3LjM5MWMwLDQuODA2LTMuODk2LDguNzAyLTguNzAxLDguNzAyaC04LjcwMyBjLTQuODA5LDAtOC43MDItMy44OTYtOC43MDItOC43MDJ2LTkuODYzYzAtNC44MDYsMy44OTYtOC43MDMsOC43MDItOC43MDNoOC43MDNjNC44MDYsMCw4LjcwMSwzLjg5Niw4LjcwMSw4LjcwM1Y2Ny4zOTF6Ii8%2BIDxwYXRoIGQ9Ik04NC4xODUsMjMzLjI4NGw2My4wODQsMjkuMzM2YzEuNjMxLDAuNzU1LDMuMzY3LDEuMTM4LDUuMTYyLDEuMTM4YzIuMzM4LDAsNC42MTctMC42NjQsNi41OTgtMS45MjQgYzMuNTQ3LTIuMjY3LDUuNjY2LTYuMTMsNS42NjYtMTAuMzM0di0wLjMyMmMwLTQuNzUyLTIuNzg1LTkuMTE2LTcuMDk2LTExLjExOGwtMzkuNDU1LTE4LjMzMmwzOS40NTUtMTguMzM0IGM0LjMxMS0yLjAwNCw3LjA5Ni02LjM2Nyw3LjA5Ni0xMS4xMTd2LTAuMzE5YzAtNC4yMS0yLjExOS04LjA3NS01LjY2Ni0xMC4zMzRjLTEuOTYxLTEuMjUzLTQuMjQ2LTEuOTE2LTYuNjA1LTEuOTE2IGMtMS43NzksMC0zLjU2MywwLjM5MS01LjE2LDEuMTMzbC02My4wOCwyOS4zMzNjLTQuMzA3LDIuMDA0LTcuMDksNi4zNjktNy4wOSwxMS4xMTd2MC44NzcgQzc3LjA5MywyMjYuOTA5LDc5Ljg3NCwyMzEuMjcyLDg0LjE4NSwyMzMuMjg0eiIvPiA8cGF0aCBkPSJNMTY1LjI1NywyOTMuMDM2YzIuMzAxLDMuMTQ5LDYuMDAyLDUuMDMsOS45LDUuMDNoMC4zMTZjNS4zNTIsMCwxMC4wNDEtMy40MjYsMTEuNjcyLTguNTE3TDIyOC43LDE2MC43ODggYzEuMTkyLTMuNzE2LDAuNTMxLTcuODE4LTEuNzcxLTEwLjk3M2MtMi4zMDEtMy4xNS02LjAwMi01LjAzLTkuOTAxLTUuMDNoLTAuMzE1Yy01LjM1NCwwLTEwLjA0OCwzLjQyNS0xMS42NzksOC41MTYgbC00MS41NTksMTI4Ljc3MUMxNjIuMjkyLDI4NS43OTMsMTYyLjk1OCwyODkuODg5LDE2NS4yNTcsMjkzLjAzNnoiLz4gPHBhdGggZD0iTTIyNy40OSwxOTIuMjc2YzAsNC43NDUsMi43ODMsOS4xMDksNy4wOTUsMTEuMTIzbDM5LjQ1NSwxOC4zMjlsLTM5LjQ1NSwxOC4zM2MtNC4zMSwyLjAwNC03LjA5NSw2LjM2OC03LjA5NSwxMS4xMTggdjAuMzIyYzAsNC4yMDUsMi4xMTcsOC4wNjgsNS42NjgsMTAuMzM2YzEuOTc0LDEuMjU4LDQuMjU0LDEuOTI0LDYuNTk1LDEuOTI0YzEuNzkzLDAsMy41MjgtMC4zODMsNS4xNy0xLjE0Mmw2My4wOC0yOS4zMzUgYzQuMzA3LTIuMDA5LDcuMDktNi4zNzIsNy4wOS0xMS4xMTV2LTAuODc3YzAtNC43NDgtMi43ODMtOS4xMTMtNy4wOTQtMTEuMTE3bC02My4wOC0yOS4zMzMgYy0xLjU5MS0wLjc0LTMuMzczLTEuMTMxLTUuMTUyLTEuMTMxYy0yLjM1NSwwLTQuNjQzLDAuNjYxLTYuNjA0LDEuOTEyYy0zLjU1MSwyLjI2My01LjY3LDYuMTI3LTUuNjcsMTAuMzM3djAuMzE4SDIyNy40OSBMMjI3LjQ5LDE5Mi4yNzZ6Ii8%2BIDwvZz4gPC9nPiA8L2c%2BIDwvZz4KDTwvc3ZnPg%3D%3D%2Chtml%2Fcss%2C%3B" alt="Cubby's Tech Stack" />

## 🧠 Resources Used
We used several resources during the development of Cubby.

#### ✅ Project Management 
- **Trello**: Used to manage each sprint
- **Figma**: Used to track and monitor frontend development

#### 💡 Frontend Development
- [**Bootstrap documentation**](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

#### ⚙️ Backend Development
- [**Django documentation**](https://docs.djangoproject.com/en/5.1/)
- [**Django models video**](https://www.youtube.com/watch?v=RbJOmgTX63M)
- [**Django views and URLs video**](https://www.youtube.com/watch?v=HyN51x01Ve8)
- [**Select-2 documentation**](https://select2.org/getting-started/installation)
- [**jQuery installation**](https://www.w3schools.com/jquery/jquery_get_started.asp)

## 📸 Images Used
Since this is a school project, and we will not be selling rights or usage of our project in any way, the images used are directly borrowed from the Internet. The links for all images used in this project will be listed below to give as much credit to the original creators as possible.
- [**Logo Image**](https://www.instagram.com/joni_marriott/)
- [**Hero Image**](https://www.istockphoto.com/illustrations/graphic-designer-at-work?page=2)

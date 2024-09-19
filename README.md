# desktop-pet v1.2.0
A "pet" that is displayed on your desktop. This project serves no practical use whatsoever. Jk it's for ADHD.

## Current Features:
- Draggable
- Plays an idle, and two walking animations. Pressing `SPACE_BAR` changes the animation.

![pet_miku_movement](https://github.com/user-attachments/assets/41830fc7-8c34-42ba-bfa6-f2bc7adec193)


## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/naixsu/desktop-pet.git
```

### 2. Install Dependencies

Navigate to the cloned directory and install the required Python packages:


```bash
pip install -r requirements.txt
```

### 3. Run the Application

In the cloned directory, execute the script to start the application:


| OS         | Command                                       |
| ------     | ----------------------------------------------|
| All        |<br><pre lang="bash">python pet.py</pre></br>  |
| Windows    |<pre lang="bash">bin/angkal</pre>              |



## Customizing the Application

You can modify the script to customize your experience:

- Change GIF Files: Stored in the `GIFS` array. Currently, the animation supports `idle.gif`, `walk_f.gif`, and `walk_b.gif`. Unfortunately, the walking GIFs are **CASE SENSITIVE**. Might make them not case sensitive in the future. If you just want one GIF to play, then you can simply remove the last two GIF paths in the `GIFS` array and add in your desired GIF.
- Adjust GIF Speed: Change the `self.ms` variable in the code to set the speed of the GIF. This is the delay between frame updates in milliseconds. Currently, there are arbitrary speeds that cater towards making the animations smooth. This variable might vary.

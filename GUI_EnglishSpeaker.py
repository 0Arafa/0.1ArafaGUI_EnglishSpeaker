import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QLineEdit, QMessageBox, QComboBox, QHBoxLayout, QTextEdit, QScrollArea
)
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter
from PyQt5.QtCore import Qt
from gtts import gTTS
from playsound import playsound
from os import remove, getcwd

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.startColor = QColor("#0f0f0f")
        self.endColor = QColor("#3f3f3f")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        gradient.setColorAt(0.0, self.startColor)
        gradient.setColorAt(1.0, self.endColor)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

class TextToSpeechGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Speech to Text Game')
        self.setGeometry(100, 100, 900, 700)

        # CentralWidgetWithGradientBackground
        self.central_widget = GradientWidget(self)
        self.setCentralWidget(self.central_widget)

        self.author_info = """
        <h2 style='color: #ffffff; text-align: center;'>Author Information</h2>
        <p style='color: #ffffff; text-align: center;'><b>Coded By:</b> Abd Almoen Arafa (0.1Arafa)</p>
        <p style='color: #ffffff; text-align: center;'><b>Country:</b> Syria</p>
        """

        self.initUI()

        self.main_text = ""
        self.points = 0
        self.sound_playing = False
        self.game_counter = 0
        self.history = []
        self.slow = False

    def initUI(self):
        # TitleLabel
        self.title_label = QLabel("Speech to Text Game", self)
        self.title_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #ffffff; background-color: #333333; padding: 20px; border-radius: 10px;")

        # DifficultyLayout
        self.difficulty_label = QLabel("Select Difficulty Level", self)
        self.difficulty_label.setFont(QFont("Arial", 24))
        self.difficulty_label.setStyleSheet("color: #ffffff;")

        self.difficulty_menu = QComboBox(self)
        self.difficulty_menu.addItems(["Easy", "Medium", "Hard", "Expert/Very Hard", "Legend"])
        self.difficulty_menu.setFont(QFont("Arial", 20))
        self.difficulty_menu.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border-radius: 15px;
                background-color: #333333;
                color: #ffffff;
                border: 2px solid #cccccc;
                selection-color: #ffffff;
                selection-background-color: #555555;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # SpeechSpeedLayout
        self.speed_label = QLabel("Select Speech Speed", self)
        self.speed_label.setFont(QFont("Arial", 24))
        self.speed_label.setStyleSheet("color: #ffffff;")

        self.speed_menu = QComboBox(self)
        self.speed_menu.addItems(["Normal", "Slow"])
        self.speed_menu.setFont(QFont("Arial", 20))
        self.speed_menu.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border-radius: 15px;
                background-color: #333333;
                color: #ffffff;
                border: 2px solid #cccccc;
                selection-color: #ffffff;
                selection-background-color: #555555;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.speed_menu.currentIndexChanged.connect(self.set_speech_speed)

        # StartGameButton
        self.start_button = QPushButton("Start Game", self)
        self.start_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1f4037;
                color: white;
                border-radius: 25px;
                padding: 15px 30px;
                border: 2px solid #1f4037;
            }
            QPushButton:hover {
                background-color: #17b978;
            }
        """)
        self.start_button.clicked.connect(self.start_game)

        # RestartButton
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.restart_button.setStyleSheet("""
            QPushButton {
                background-color: #4e4e4e;
                color: white;
                border-radius: 25px;
                padding: 15px 30px;
                border: 2px solid #4e4e4e;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
            }
        """)
        self.restart_button.clicked.connect(self.restart_game)
        self.restart_button.setEnabled(False)

        # PointsLabel
        self.points_label = QLabel("Your Points: 0", self)
        self.points_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.points_label.setStyleSheet("color: #ffffff; background-color: #333333; padding: 15px; border-radius: 10px;")

        # GameCounterLabel
        self.game_counter_label = QLabel("Game Counter: 0", self)
        self.game_counter_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.game_counter_label.setStyleSheet("color: #ffffff; background-color: #333333; padding: 15px; border-radius: 10px;")

        # UserInput
        self.answer_label = QLabel("Your Answer:", self)
        self.answer_label.setFont(QFont("Arial", 24))
        self.answer_label.setStyleSheet("color: #ffffff;")

        self.answer_entry = QLineEdit(self)
        self.answer_entry.setFont(QFont("Arial", 20))
        self.answer_entry.setStyleSheet("""
            padding: 15px;
            border-radius: 10px;
            background-color: #ffffff;
            color: #333333;
            border: 2px solid #cccccc;
        """)
        self.answer_entry.returnPressed.connect(self.submit_answer)

        # SubmitButton
        self.submit_button = QPushButton("Submit Answer", self)
        self.submit_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0f4c75;
                color: white;
                border-radius: 25px;
                padding: 15px 30px;
                border: 2px solid #0f4c75;
            }
            QPushButton:hover {
                background-color: #3282b8;
            }
        """)
        self.submit_button.clicked.connect(self.submit_answer)
        self.submit_button.setEnabled(False)

        # HistoryButton
        self.history_button = QPushButton("History", self)
        self.history_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.history_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 25px;
                padding: 15px 30px;
                border: 2px solid #d32f2f;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        self.history_button.clicked.connect(self.show_history)

        # StatusLabel
        self.status_label = QLabel(self)
        self.status_label.setFont(QFont("Arial", 20))
        self.status_label.setStyleSheet("color: #ffffff;")
        self.status_label.setWordWrap(True)

        # AuthorInformationLabel
        self.author_label = QTextEdit(self.author_info, self)
        self.author_label.setFont(QFont("Arial", 16))
        self.author_label.setStyleSheet("color: #ffffff; background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.author_label.setReadOnly(True)

        # Layouts
        difficulty_layout = QHBoxLayout()
        difficulty_layout.addWidget(self.difficulty_label)
        difficulty_layout.addWidget(self.difficulty_menu)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_menu)

        game_controls_layout = QVBoxLayout()
        game_controls_layout.addWidget(self.start_button)
        game_controls_layout.addWidget(self.restart_button)
        game_controls_layout.addWidget(self.points_label)
        game_controls_layout.addWidget(self.game_counter_label)
        game_controls_layout.addWidget(self.answer_label)
        game_controls_layout.addWidget(self.answer_entry)
        game_controls_layout.addWidget(self.submit_button)
        game_controls_layout.addWidget(self.status_label)
        game_controls_layout.addWidget(self.history_button)
        game_controls_layout.setAlignment(Qt.AlignCenter)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.title_label)
        info_layout.addLayout(difficulty_layout)
        info_layout.addLayout(speed_layout)
        info_layout.addStretch(1)
        info_layout.addWidget(self.author_label)
        info_layout.setAlignment(Qt.AlignTop)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.addLayout(info_layout, 1)
        main_layout.addLayout(game_controls_layout, 2)
        main_layout.setContentsMargins(50, 50, 50, 50)

    def set_speech_speed(self):
        self.slow = self.speed_menu.currentText() == "Slow"

    def start_game(self):
        if not self.sound_playing:
            self.main_text = self.generate_text()
            self.play_text(self.main_text)
            self.answer_entry.clear()
            self.status_label.setText("")
            self.submit_button.setEnabled(True)
            self.sound_playing = True
            self.game_counter += 1
            self.game_counter_label.setText(f"Game Counter: {self.game_counter}")
            self.restart_button.setEnabled(False)

    def restart_game(self):
        self.points = 0
        self.game_counter = 0
        self.points_label.setText("Your Points: 0")
        self.game_counter_label.setText("Game Counter: 0")
        self.history.clear()
        self.restart_button.setEnabled(False)
        QMessageBox.information(self, "Info", "Game has been reset. Start a new game to play again.")

    def generate_text(self):
        text="cat.dog.sun.moon.star.tree.car.book.pen.hat.shoe.cup.bed.ball.fish.apple.bird.cake.chair.door.frog.grass.house.kite.leaf.milk.mouse.pencil.rain.road.ship.soap.spoon.table.train.water.window.boat.bread.cloud.corn.dress.flower.hand.horse.ice.lamp.map.nest.snow.bike.baby.egg.farm.game.girl.hill.jam.king.lamb.lion.man.owl.park.queen.ring.sock.truck.van.wave.yard.zebra.ant.bear.cow.duck.ear.fire.goat.hat.ink.jar.key.leg.moon.nose.orange.pig.quilt.rock.sun.top.umbrella.vase.wolf.ax.box.cake.dish.eye.frog.gum.hen.iron.jug.kite.log.mop.net.ox.pan.rug.sock.tent.urn.well.yarn.zip.apple.ball.drum.elf.fan.gum.ice.jam.kite.leaf.mop.owl.pie.quill.rat.sun.top.urn.vase.web.x-ray.yak.zoo.bear.cat.dog.egg.fox.goat.hen.ink.jar.key.log.mop.net.ox.pan.rug.sock.tent.urn.well.yarn.zip.april.bat.cup.drum.elf.fan.gum.hen.ink.jar.kit.log.mat.nut.owl.pie.quill.rat.sun.top.urn.vase.web.x-ray.yak.zoo.april.box.car.dog.elf.fan.gum.hen.ink.jug.key.log.mat.nut.owl.pie.quill.rat.sun.top.urn.vase.web.yak.zoo.name.will you hold on.even if.door.window.roof.stairs.carpet.bed.bad.both.perfume.look at me.battle.war.when you light the candle.got the music in you baby tell me why.motion.picture.it's leading me on.soundtrack.opera house.blessed.curse.drown.throne.the final episode.scream.aim.fire.true friends.bad idea.dead girl in the pool.reach out.fit in with.listen to me.loyal.honest.values first.pray.smile.london.apocalypse.monsters.eagle.master.royal.jenny.henry.lucas.t-shirt.captain black.ungrateful.don't lean on me.disposable.can i call you tonight.dumb.flash.nothing's gonna hurt you baby.pistol.don't hurt me.seventeen.upside down.dead but pretty.fight this.lips.apartment.depression.stupid.unanswered.reflection.build.sugar.salt.salty.reasons to.pretty.shape.tell me about you.late night.winter.shine a light.trapped.until we leave the ground.crying in your sweater.afraid.lonely.sunflower.youth.mountain.covered.i know you so well.my girl.your girl.our girl.you make it worse.bleeding out.cinnamon.instrumental.voices.firefighter.cannonball.say goodbye.empty.puppets.snow.scissor.cycle.rats.city lights.will you still love me.negative.before i forget.moonlight.sicko mode.crime.promise me.last of us.worn out.the other side.teardrops.go to hell.for heaven's sake.alison.control.issues.money.addicted.left behind.the devil in i.hive mind.you broke my heart again.heart of glass.squeeze.mercury.black blood.born to die.where do lovers go.the city holds my heart.placeholder.jealous.space.call me.miss you.sometimes it ends.in the end.affection.sunsetz.dreaming of you.starry eyes.what can i say.attention.moral of the story.fade into you.almost.shadow.theme.diary.fly me to the moon.sport.godzilla.parasite.god knows i tried.high by the beach.sniff.smell.honeymoon.send me an angel.after dark.sweater weather.free.highway.inside out.sing.natural.thunder.a dark knight.touch my back and i'll touch yours.sunlight on your skin.ghostly kisses.backwards.punch.shine.sam.medicine.some say.somewhat interesting.the brightside.save that shit.gym class.don't be weak.nasty names.ring.line without a hook.let go.cry alone.airplanes.white tee.change your mind.say yes to heaven.beat it.smooth criminal.sorry for me.don't be sad.come a little closer.cruel world.regret.just in case.watch.me and the birds.switch up.don't be mad.violent dreams.florida.lost cause.new flesh.out of my league.sweet dreams.white noise.bubblegum.make me famous.the blonde.die hard.tell my mother i'm sorry.move on.be strong.middle east.up up and away.end my life.crazy.wait a minute.crush on you.i love you baby.weird.catch.swim.faceless.fed up.the perfect.radio.summertime sadness.a little death.i just wanna be your sweetheart.you said.too close.zombie.i can't find anyone.message man.give me your heart.kiss your hand.to infinity.let me get what i want.electric feel.jungle.in your arms.take me home.country roads.christmas kids.my time is here.and i'll make it clear.spit in your face.one last time.there is a light that never goes out.crashes into us.to die by your side.is such a heavenly way to die.oh i love you my dear.but i'm gone.i might come back.i could stop time.sleep on the floor.open your eyes.thank you.my own summer.wicked game.we fell in love in october.mary on a cross.thank you.be quiet and drive.live forever.best person you know.haunted.all girls are the same.look up.want me.i was all over her.bones.freak show.fall back.first love.late spring.let it happen.save me.faster.harder.right here.runaway.hide your kids.when it happen.when the devil speaks.south west.convert.psychosocial.american psycho.chinatown.forrest gump.taxi driver.baby blue movie.stop waiting.placement.come right back.i've been waiting for you.in trouble.when you know you know.and share my body.and share my mind.with you.no.yes.sure.happy.mode.gold.silver.paste.past.copy.move.movies.moon.can i get you the moon.was come on for you.car.window.metal.wood.turtle.lion.eagle.jaguar.shark.snake.block.tent.maybe.error.present.after.both.before.put.castle.bad guy.age.how much.it's a hard work.you always be my day one.don't really wanna die i just wanna feel alive.how long.how many.steam.stream.live.govern.about.long.this.around.play.by.these.those.this.at.now.own.give.look at me.life.nano.science.exit.quit.black screen.blue screen.white screen.park.part.party.pretty.pretty face.so much fun.each.approach.increase.ability.benefits.fit girl.fat girl.fit boy.fat boy.point.enter.star.stick.toxic.nine.has been.society.fuck society.thankful.apple.orange.i got you.did you get it.say hello for me.where are you from.how old are you.what's your name.do you like sciences.do you like the music.rockbye baby.don't cry please.just like this.it was the end.best movies.shorts.shoes.the end.you're my day one.come and smell this flower.i'll eat this.are you here.is she there.hello,how are you today.are you okay.don't look at me like this.it's a bad feelings.it's your cat or what.i'm going to my home.wide pool.world wide.nice tree.around the world.all over the world.come here boy.come here girl.what's your favourite color.peace out.rest in peace.it's a nice car.purple car.green car.hot wheels.turkey.england.syria.egypt.algeria.america.colombia.germany.africa.middle east.canada.moroco.lebanon.iraq.middle east servers.europe.open this file.heaven.darkest day.give me the loop.high performance.large icon.low battery.don't run away.look at me.locked phone.hard battle.nice game.thug life.a lot of money.there is a cd there.the floor is too long.what is your language.i like this wall.let's make some noise.beautiful table.she's the tallest woman.are you there.bodybuilding is dangerous when playing fault.stop please.read this.turn off this computer.turn on the ps4.her hair is too long.she's a blonde woman.blue eyes.let's play together on this phone.don't run while the weather is stormy.it was a hard day.just read this.study for your test.you just want attention.trust me.can i get you the moon.sunshine.machine.application.exciting challenge.let's go.i don't know.i know it.i swear to god.animal.generator.purple.what the fuck.may i help you.can i see you.click here.this is for test.how are you.is that you.how old are you.ok thank you.come on over in my direction.isn't lovely all alone.baby don't leave me.begginer.are you a human.i think he's right.ok peace.see you later.i can't hold on.i'm waiting for you.hang on.please don't break my heart.he's a boy.boy.she's a girl.girl.maths.numbers.are you alone.bullshit.you're right.fault.alive.can you hate me.i love you.my mom.i love that.sky.the sky is high.key.robot.dark.high building.weight.password.email.raise of nations.general.computer.are you a child.children.television.one hundred.thousands of people.lover.i can't wait for it.control.touchpad.character.mother.father.son.family.daughter.cousin.grandmother.grandfather.nice body.cute one.he's a tall man.i like him.i like her.is she need me.need is need.fire.sing with me.what is the best song for you.singer.female.male.make.made.cooking.my mom's cooking a nice food.cheese.meeting.mate.university.school.primary school.dog.cat.turtle.airplane.telephone.house.uniform.notebook.book.horor.pencil.afraid.changes.i won't let you go.let me love you.kill the monster.don't play this game again.do you wanna come with me.yes write this.no man i don't like it.under the sea.brown skin.white leather.let's drink this.are you ready.refresh.guide book.restaurant.sort by.view.quickly please.nice clothes.hot food.spicy food.deep sea.adult man.adult woman.oldman.oldwomen.group of youngs.baby you can hold me.bettery.charger.telephone.light.motion.easly.fast.create.chat.zoom.zoo.input.output.display.desktop.launcher.join us.call me later.as tall as.meeting.angry.after.again.also.against.area.baby.away.bad.bag.boy.agency.although.above.about.add.address.affect.administrator.hungry.east.west.south.north.different.island.fairly.juice.kiss.knife.rain.bury.damage.umbrella.violent.wire.worth.worst.ugly.teach.learn.safe.safely.rainbow.library.cartoon.network.awesome.huge.healthy.handsome.gentle.delicious.energy.famous.family.farm.from.camera.careful.carefully.attractive.bigger.fitter.but".split(".")
        List = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
        level = self.difficulty_menu.currentText().lower()
        if level == "easy":
            main_text = random.choice(text)
        elif level == "medium":
            many = random.choice(List[1:3])
            answer = random.choices(text, k=many)
            main_text = " ".join(answer)
        elif level == "hard":
            many = random.choice(List[3:6])
            answer = random.choices(text, k=many)
            main_text = " ".join(answer)
        elif level == "expert/very hard":
            many = random.choice(List[6:10])
            answer = random.choices(text, k=many)
            main_text = " ".join(answer)
        elif level == "legend":
            many = List[10]
            answer = random.choices(text, k=many)
            main_text = " ".join(answer)
        return main_text

    def play_text(self, text):
        try:
            speaker = gTTS(text=text, lang="en", slow=self.slow)
            speaker.save("audio.mp3")
            playsound(f"{getcwd()}\\audio.mp3")  # SoundPlaying
            remove("audio.mp3")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error, Please Check Your Internet Connection and Try Again, Error Info: {e}")

    def submit_answer(self):
        if self.sound_playing:
            user_answer = self.answer_entry.text().strip()
            correct = user_answer.lower() == self.main_text.lower()
            if correct:
                self.points += 1
                self.status_label.setText("Correct (;")
                self.status_label.setStyleSheet("font-size: 20px; color: #4caf50; background-color: #ffffff; border-radius: 10px; padding: 10px;")
            else:
                self.points -= 1
                self.status_label.setText(f"{self.main_text}")
                self.status_label.setStyleSheet("font-size: 20px; color: #f44336; background-color: #ffffff; border-radius: 10px; padding: 10px;")
            self.points_label.setText(f"Your Points: {self.points}")
            self.points_label.setStyleSheet("color: #ffffff; background-color: #333333; padding: 15px; border-radius: 10px; font-weight: bold;")
            self.history.append({
                "counter": self.game_counter,
                "difficulty": self.difficulty_menu.currentText(),
                "user_answer": user_answer,
                "correct_answer": self.main_text,
                "result": "Correct" if correct else "Wrong"
            })
            self.sound_playing = False
            self.submit_button.setEnabled(False)
            self.restart_button.setEnabled(True)
        else:
            QMessageBox.information(self, "Info", "Please start a game first.")

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "History", "No history available yet.", QMessageBox.Ok)
            return

        history_text = """
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ffffff;
                text-align: left;
                color: #ffffff;
            }
            th {
                background-color: #555555;
            }
            tr:nth-child(even) {
                background-color: #333333;
            }
        </style>
        <h2 style='color: #ffffff;'>History</h2>
        <table>
            <tr>
                <th>Game</th>
                <th>Difficulty</th>
                <th>Your Answer</th>
                <th>Correct Answer</th>
                <th>Result</th>
            </tr>
        """
        for record in self.history:
            result_color = "#4caf50" if record["result"] == "Correct" else "#f44336"
            history_text += f"""
                <tr>
                    <td>{record['counter']}</td>
                    <td>{record['difficulty']}</td>
                    <td>{record['user_answer']}</td>
                    <td>{record['correct_answer']}</td>
                    <td style='color: {result_color};'>{record['result']}</td>
                </tr>
            """
        history_text += "</table>"
        
        scroll = QScrollArea()
        history_content = QLabel(history_text)
        history_content.setStyleSheet("background-color: #2c2c2c; padding: 20px;")
        scroll.setWidget(history_content)
        scroll.setWidgetResizable(True)
        scroll.setMinimumSize(800, 600)

        dialog = QMainWindow(self)
        dialog.setWindowTitle("History")
        dialog.setCentralWidget(scroll)
        dialog.resize(850, 650)
        dialog.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    game = TextToSpeechGame()
    game.show()
    sys.exit(app.exec_())

#By: Abd Almoen Arafa(0.1Arafa)

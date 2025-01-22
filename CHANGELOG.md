# CHANGELOG


## v0.7.4 (2025-01-22)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`93c8b4a`](https://github.com/jocokiss/Adventure_game/commit/93c8b4a458eef07b8778989fa22685d24957db43))


## v0.7.3 (2025-01-22)

### Bug Fixes

* fix(API): fix wsgi.py ([`319ad25`](https://github.com/jocokiss/Adventure_game/commit/319ad25ef797d47a619e70ba92c8d7997a19c2ec))

* fix(API): fix deployment issue ([`2d29069`](https://github.com/jocokiss/Adventure_game/commit/2d290690ae06e1a03fb34174017edb027b76f5a3))


## v0.7.2 (2025-01-22)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`f553cb6`](https://github.com/jocokiss/Adventure_game/commit/f553cb6eada7888cd19837e3e88308f390acc0d2))


## v0.7.1 (2025-01-22)

### Bug Fixes

* fix(API): Add missing dependency ([`d70f99c`](https://github.com/jocokiss/Adventure_game/commit/d70f99c0c087a2f8012b4cf1c443a3e1aea8e019))

* fix(API): Add missing requirements.txt ([`3bd6489`](https://github.com/jocokiss/Adventure_game/commit/3bd6489b16edb367f4ec972ad22bb973193fa689))


## v0.7.0 (2025-01-22)

### Code Style

* style(CONFIG): Make private method from get_object() ([`06d426c`](https://github.com/jocokiss/Adventure_game/commit/06d426cc1a8cb8006a0e3ba165913b3d9700e0bf))

### Features

* feat(API): Introduce API ([`2838c37`](https://github.com/jocokiss/Adventure_game/commit/2838c37c5130cd8c059b722459279a020227eff8))

### Unknown

* Merge pull request #6 from jocokiss/feature/api

feat(API): Introduce API ([`038ad2d`](https://github.com/jocokiss/Adventure_game/commit/038ad2d649c43853b41b468b1fb96f933fcc8573))

* Merge branch 'refs/heads/feature/ui' ([`7a0f201`](https://github.com/jocokiss/Adventure_game/commit/7a0f2017058569b11652e14218a3d83204003d59))


## v0.6.0 (2025-01-21)

### Code Style

* style(CONFIG): Change the way coordinates are set ([`642117f`](https://github.com/jocokiss/Adventure_game/commit/642117f4c2d6ecdf99ed3a435fb8a34c5202a26d))

* style(RENDER_HEALTH): Maka the render_health method a private method ([`118b7eb`](https://github.com/jocokiss/Adventure_game/commit/118b7eb9f70c3f26d759bdd109b45779f5abaeb9))

### Features

* feat(GAME-UI): Add xp bar and streamline processes

Add xp bar. Change the way coordinates are saved. Change the way tiles are loaded. Load real player stats. ([`fb81673`](https://github.com/jocokiss/Adventure_game/commit/fb81673f23fac1fb44403110b8c2f82d4aa84390))

* feat(DATACLASSES): Add simple way to initialize the Coordinates dataclass ([`2f7afe6`](https://github.com/jocokiss/Adventure_game/commit/2f7afe6b6cf21bd85196fcc1924740461b6e0e34))

* feat(COMBAT): Add more logic to combat attributes

Add properties for valuable data. Add mechanism to gain xp and lvl up. ([`12764da`](https://github.com/jocokiss/Adventure_game/commit/12764da79d3229f973a2c7d2d5e3ef486c7967fd))

* feat(HEALTH-BAR): Implement health bar for UI. Hearts dinamically change with health percentage ([`45a70ca`](https://github.com/jocokiss/Adventure_game/commit/45a70ca497194b9ac732dd15c271cb4914407d12))

* feat(HEALTH-BAR): Add health bar. Still need to handle the different percentages of health ([`1dc039d`](https://github.com/jocokiss/Adventure_game/commit/1dc039df04aca8f36b01b4dca6e0f5846f5b5a13))

* feat(LVL-BAR,-LVL): Add level bar and lvl indicator to UI ([`9ab3b1e`](https://github.com/jocokiss/Adventure_game/commit/9ab3b1e4f97a3b61e7959e7267919e6996f2e60a))

### Refactoring

* refactor(TILED): Change the way StaticObjects store data ([`8215165`](https://github.com/jocokiss/Adventure_game/commit/8215165f8db24a93c89bca0e9b9e0c34a684fb43))

* refactor(GAME-UI): Rename some functions, remove some comments ([`f3868d1`](https://github.com/jocokiss/Adventure_game/commit/f3868d1446f8074d921075553fc2175393d3fe0a))

* refactor(LOAD-FROM-TILESET): Refactor the way tilesets are loaded from file ([`f48a538`](https://github.com/jocokiss/Adventure_game/commit/f48a538c3f2622fd5636258324da4731831c955e))

### Unknown

* Merge pull request #5 from jocokiss/feature/ui

Feature/UI ([`ebaf29f`](https://github.com/jocokiss/Adventure_game/commit/ebaf29fac990e35d3a44f89746a3b2655fe3002f))


## v0.5.1 (2025-01-20)

### Bug Fixes

* fix(COLLISION): Fix issue where tile borders wont count as collision ([`4c477a3`](https://github.com/jocokiss/Adventure_game/commit/4c477a3cccae4bec3955e21b8361ad1e2d155057))


## v0.5.0 (2025-01-16)

### Code Style

* style(gitignore): Update .gitignore ([`9b6ca1b`](https://github.com/jocokiss/Adventure_game/commit/9b6ca1bcaa8c2b4a1fcadae4955bf893f2be5839))

### Features

* feat(COMBAT): Add combat to the game. It is primitive but working ([`542d42e`](https://github.com/jocokiss/Adventure_game/commit/542d42e2643e6fb4a467ec77715e08a91394984a))

### Refactoring

* refactor(Architecture): Restructure codebase to make it more readable ([`ecab5e5`](https://github.com/jocokiss/Adventure_game/commit/ecab5e527ffa0d74a57097736394e65673275e47))

### Unknown

* Merge branch 'feature/restructure' ([`f17b76f`](https://github.com/jocokiss/Adventure_game/commit/f17b76f7ff7684b1b13074779f81dfdac4728851))


## v0.4.0 (2025-01-16)

### Features

* feat(COMBAT): Add combat state to the game, rearrange structure for better understanding ([`0559dab`](https://github.com/jocokiss/Adventure_game/commit/0559dab70d799ee29ae42abe1890e6775fb6a9df))

* feat(NPC): Add IDLE animation to NPC, also when in range make the NPC interactable ([`0216b49`](https://github.com/jocokiss/Adventure_game/commit/0216b49c928a5b99bbc8eb02c88cfaaa2b742a97))

* feat(NPC): Add NPC to the game, render it on the map and make it move ([`cd0010a`](https://github.com/jocokiss/Adventure_game/commit/cd0010ab6def7e6a43f368f4c2290e169ed1097e))

* feat(NPC-class): Create abstract class from Sprites. From the abstract class create Player and NPC classes. ([`930b6c6`](https://github.com/jocokiss/Adventure_game/commit/930b6c62be752be4f056afb7b2330b478ac1e403))

### Refactoring

* refactor(version-control,-basic-game): remove redundant import from basic_game.py  and redundant section from workflow ([`f0566d6`](https://github.com/jocokiss/Adventure_game/commit/f0566d6133ba7fd39ee2bc063e53b7aadbd60948))


## v0.3.0 (2025-01-08)

### Features

* feat(gameplay): add main menu to the game

Main menu has been added to the game. Now it is possible to start a new game, load game(not functioning yet) and go back to the main menu, which is effectively restarts the gaming session so you can either start a new game or load a saved one. ([`84c5574`](https://github.com/jocokiss/Adventure_game/commit/84c5574284cedc55f4aef3d891e6c6b39ce46f06))


## v0.2.2 (2025-01-08)

### Bug Fixes

* fix(pyproject.toml): remove old instances of changelog entry ([`61ccb3b`](https://github.com/jocokiss/Adventure_game/commit/61ccb3b88c8d27cc8a6a46152a99d31577c7464e))


## v0.2.1 (2025-01-08)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`e88ba91`](https://github.com/jocokiss/Adventure_game/commit/e88ba917601f5cf8e79fef89dcdf705915dbf331))


## v0.2.0 (2025-01-08)

### Bug Fixes

* fix(workflows): Add debug section to workflow to better understand issues ([`afde0fc`](https://github.com/jocokiss/Adventure_game/commit/afde0fca5add640b5630d9f0225bfef991a3c6f7))

* fix(asd): fix actino ([`580e00f`](https://github.com/jocokiss/Adventure_game/commit/580e00fd53b8dbbd420863def99045e9b54dcdbd))

* fix(pyproject.toml): add version_source = 'tag' to configuration ([`c0b26ef`](https://github.com/jocokiss/Adventure_game/commit/c0b26ef9e0b81496dc904da6abb4ee819e7dd3a2))

* fix(git): add git tag and push it to remote repository ([`6cc0033`](https://github.com/jocokiss/Adventure_game/commit/6cc00339e92be7ba8ed952fa66c2ab2309199f4e))

### Code Style

* style(setup.py): remove trailing whitespace at the end ([`a28c436`](https://github.com/jocokiss/Adventure_game/commit/a28c4365c2ea4446ec13d9aa358beb436ffd28a6))

### Documentation

* docs(CHANGELOG.md): New entry was created ([`bdaa185`](https://github.com/jocokiss/Adventure_game/commit/bdaa185e1ac2b05bfcc557f694e7ce3c51dfe7a0))

### Features

* feat(action-file): change github action ([`d63674d`](https://github.com/jocokiss/Adventure_game/commit/d63674d3f40927dc55e7f7f519ad3a842a7fa164))


## v0.1.0 (2025-01-08)

### Breaking

* feat(project): add github action for version-controlling

BREAKING CHANGE: ([`4a549e2`](https://github.com/jocokiss/Adventure_game/commit/4a549e2ec170df1e5647a653b58ca922124ee275))

### Bug Fixes

* fix: remove local path from pyproject.yaml ([`ec61e69`](https://github.com/jocokiss/Adventure_game/commit/ec61e69a342e5242dc84ebfcb9e0f7cbae0f4783))

* fix: asdfg ([`bfed2ad`](https://github.com/jocokiss/Adventure_game/commit/bfed2ad52f34a1a98312801a9d7f20b8ed5e5b05))

* fix: qwe ([`61cbe29`](https://github.com/jocokiss/Adventure_game/commit/61cbe293cc70e93e72e69ccdbed8dc0e99d68ed4))

* fix: asd ([`631a0b3`](https://github.com/jocokiss/Adventure_game/commit/631a0b3129aa8a052cb2495e321e8242cf46b3a7))

* fix: asd ([`3a2a2a6`](https://github.com/jocokiss/Adventure_game/commit/3a2a2a69b510fe5b505862fceadda2d2847d178a))

* fix: asd ([`317dfaa`](https://github.com/jocokiss/Adventure_game/commit/317dfaa492eb552d3bafda5f04c1e9c58f90c4ac))

* fix: asd ([`6afde06`](https://github.com/jocokiss/Adventure_game/commit/6afde061951d47df9c46a1a2a4c4edb83675af93))

* fix: bug fix ([`41bea7c`](https://github.com/jocokiss/Adventure_game/commit/41bea7c32289493ddf1e48f210c72d09a6657356))

* fix: toml fix ([`2b0f4b7`](https://github.com/jocokiss/Adventure_game/commit/2b0f4b7525d9060b4b3a2533df0d7afbf9d63ab8))

* fix(pyproject.toml): version format changed from v.0.0.0 to 0.0.0 ([`8cc8c39`](https://github.com/jocokiss/Adventure_game/commit/8cc8c3976f0586002598ad8312616d51e7196046))

### Features

* feat(version-controll): try a new approach to make versioning work ([`442b7de`](https://github.com/jocokiss/Adventure_game/commit/442b7de6da85a03e29ca5403555f6e6221416b85))

* feat: something ([`ef69be3`](https://github.com/jocokiss/Adventure_game/commit/ef69be30372e201acb841f0ca65d031019c90a82))

* feat: figuring out version controll ([`1774b91`](https://github.com/jocokiss/Adventure_game/commit/1774b917146fefc44eeb737ce0120faa88361620))

* feat: add versioning to the existing project ([`59bff6e`](https://github.com/jocokiss/Adventure_game/commit/59bff6e806f998acaf88a920510075b1ccad0ca2))

* feat: add version controll to project ([`9ec9e82`](https://github.com/jocokiss/Adventure_game/commit/9ec9e82191808d7cfc66b460cb43e0fec2e978ae))

### Unknown

* Merge pull request #4 from jocokiss/feature/git_ignore_update

Feature/git ignore update ([`4c2ebaa`](https://github.com/jocokiss/Adventure_game/commit/4c2ebaa8693cd76f4646dea92e7fbcab8c918458))

* updated gitignore, removed redundant map folder ([`2c0b3b6`](https://github.com/jocokiss/Adventure_game/commit/2c0b3b65f8bcb4e60357cbbb65def38846a466a1))

* rendered background and foreground separately. Enhanced code here and there ([`8c595b4`](https://github.com/jocokiss/Adventure_game/commit/8c595b46d4504fb5cdea48a98fde0508fa975be4))

* rendered background and foreground separately. Enhanced code here and there ([`d65ecd7`](https://github.com/jocokiss/Adventure_game/commit/d65ecd7c6d5917a868a83a6f33de197a20c95f32))

* created the logic for colliding with borders, finished ([`ce4359a`](https://github.com/jocokiss/Adventure_game/commit/ce4359adfa95e3c544905b81fb20e9f6b960ca99))

* created the basic logic for colliding with borders, only works one way so far ([`8ed4b35`](https://github.com/jocokiss/Adventure_game/commit/8ed4b35c736c3f0847b2ed02a2c1af483a90d787))

* Merge pull request #3 from jocokiss/feature/splitting-up-to-modules

Feature/splitting up to modules ([`d4ab579`](https://github.com/jocokiss/Adventure_game/commit/d4ab579f05a296ed0f31ebec41ece9b4b7125402))

* character and map animated ([`1fa9410`](https://github.com/jocokiss/Adventure_game/commit/1fa941003c18381ed8b8706507e4ac2a3659cf34))

* ready for animating mapx ([`f6652dd`](https://github.com/jocokiss/Adventure_game/commit/f6652dd00ad8ddb25e5a9168233702c7c211b312))

* Movement is lit ([`feaae96`](https://github.com/jocokiss/Adventure_game/commit/feaae960ad5566f518428d2c60a30e78c46adb0d))

* Movement is finally really good. Will spend some more tim eon it tho ([`2b15d92`](https://github.com/jocokiss/Adventure_game/commit/2b15d9291c3ca1b086a3bb0d8822584e331221bd))

* movement fine for now. Next step is adding player coordinates ([`ab1b2d8`](https://github.com/jocokiss/Adventure_game/commit/ab1b2d81393a400a6f2ecd394af133aeab0a4d8e))

* a way for make it compact ([`317de9f`](https://github.com/jocokiss/Adventure_game/commit/317de9f6f9e4f56edc4ca65a420207cbf11e69b4))

* found a good solution for moving around the map ([`64657d6`](https://github.com/jocokiss/Adventure_game/commit/64657d6c5274e7471b81cf9393bd88aabb1e81ca))

* found a good solution for moving around the map ([`c9e5709`](https://github.com/jocokiss/Adventure_game/commit/c9e5709dcaa0a793aa5db07a81c03b6160d879ed))

* structure changed, somewhat working ([`6fc4c01`](https://github.com/jocokiss/Adventure_game/commit/6fc4c019077ce87c7b04a472cf4e1b28cc3b7834))

* Merge pull request #2 from jocokiss/feature/refining-basic-pygame

Feature/refining basic pygame ([`5c75480`](https://github.com/jocokiss/Adventure_game/commit/5c754808d57f9a805f07a5448f54b8c1405c8cde))

* refactoring started ([`dbd6798`](https://github.com/jocokiss/Adventure_game/commit/dbd6798cde5021714f84be36e0057f21cbcd0d3c))

* animation works! ([`ae467a4`](https://github.com/jocokiss/Adventure_game/commit/ae467a405f607fa2d5847705e90b55e5ac4f3d93))

* animated character is almost done! ([`6001319`](https://github.com/jocokiss/Adventure_game/commit/6001319a9061f62485f815aa45447adfc62ce12b))

* player coordinates can be updated now. zooming works too, Need to resolve issue with collision ([`a89f301`](https://github.com/jocokiss/Adventure_game/commit/a89f301a455677d14f6636b3ef09a2eeb4735454))

* Added tile-based movement ([`e377e1b`](https://github.com/jocokiss/Adventure_game/commit/e377e1b0b6e5032c7204480cd8a419744a628b2c))

* Merge pull request #1 from jocokiss/feature/basic_pygame

Feature/basic pygame ([`dcb6794`](https://github.com/jocokiss/Adventure_game/commit/dcb67945aa7f3ea351b9c2cde8c1db4a58c92542))

* Basic skeleton is working ([`4a1ce2b`](https://github.com/jocokiss/Adventure_game/commit/4a1ce2b21a797e58fa53489072226a0b2464e095))

* created basic skeleton ([`09bd5a1`](https://github.com/jocokiss/Adventure_game/commit/09bd5a1767025c1af6138c8fd07dc75cdad4002f))

* added gitignore ([`ae74ab4`](https://github.com/jocokiss/Adventure_game/commit/ae74ab460a9731a1f3ccbd2e5006005e562b0caa))

* Deleted old .idea ([`48c6046`](https://github.com/jocokiss/Adventure_game/commit/48c6046cf8767c1dc597304b9c4953394e1f6f2e))

* Added gitignore ([`ecb42c0`](https://github.com/jocokiss/Adventure_game/commit/ecb42c013ace9d0e5051b5703b5d1054ce1b8645))

* Added gitignore ([`f6e77c9`](https://github.com/jocokiss/Adventure_game/commit/f6e77c9d0d2ae255f41067d4b3e912d050c4c4d2))

* Added gitignore ([`52cfcde`](https://github.com/jocokiss/Adventure_game/commit/52cfcde32c862e02a6b82a8f66c3413b5171c40a))

* Added gitignore ([`4c75916`](https://github.com/jocokiss/Adventure_game/commit/4c75916411cb8497b12f5ba4473f6938ed8ff2ce))

* Delete Valeria.json ([`3f96956`](https://github.com/jocokiss/Adventure_game/commit/3f96956545492703f1c67e8e290b7c98437de125))

* Delete test.py ([`1d008db`](https://github.com/jocokiss/Adventure_game/commit/1d008dbaf2a00aba33e0ffa0fa6906ccf6c9fca2))

* added test.py ([`a59d2ba`](https://github.com/jocokiss/Adventure_game/commit/a59d2bad3472500e474a3fcc22adeb496c7cbd34))

* lol ([`e3f4d53`](https://github.com/jocokiss/Adventure_game/commit/e3f4d537aba9a78c5582049c3d490d856c8f9dfd))

* made changes ([`7d7c489`](https://github.com/jocokiss/Adventure_game/commit/7d7c489ae11531c82078b8ea97958e4fbbadaded))

* deleted test ([`abaa871`](https://github.com/jocokiss/Adventure_game/commit/abaa871c9b14e3a4e32100b3416a57624044115f))

* merges ([`a7ad630`](https://github.com/jocokiss/Adventure_game/commit/a7ad6308a7be33e1edd205c85cdb97058c2b77b8))

* added file ([`be4aa92`](https://github.com/jocokiss/Adventure_game/commit/be4aa92ba89559c04616b4eeeb8e7e81111c8ee3))

* reverted changes ([`069b542`](https://github.com/jocokiss/Adventure_game/commit/069b542a63727e7d23d53815462086cc7bafe760))

* made changes ([`b3832d7`](https://github.com/jocokiss/Adventure_game/commit/b3832d7680669b7b2ac2db18a3c5d7ed501c4a76))

* made changes ([`b390218`](https://github.com/jocokiss/Adventure_game/commit/b3902183c97a36aebea09baf840a70b7a8919d70))

* first commit on new branch ([`22ef320`](https://github.com/jocokiss/Adventure_game/commit/22ef3206ca78bd56ddfeb8dfd51c1480f3664416))

* added ingame collection ([`57564fa`](https://github.com/jocokiss/Adventure_game/commit/57564fa0184d275d682c9be0819b99e5384c2fa4))

* added adventure_game.py ([`db34191`](https://github.com/jocokiss/Adventure_game/commit/db34191440e5ae016100637767295a30451793fc))

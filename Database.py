class Database:
    database = {
        "john": {
            "hash": "613438204179c6daa43d04e32fc0509d76b87efad1bc70f84038a1065fcdb7dec3683872c35f5d20c251248db157cb9fdea16d99753476db87ca3d9db7fd6cc9",
            "salt": "5491042904581601128657979932589155499693898775280553248067569895156099593707840853134279929504198257407120492966788420727587998551497525552117164422822341",
            "voted": False},
        "owen": {
            "hash": "1cd6456f869982462b4d111f8abfb5c9c09e7a5a34c84b12c80ae5bab4514a4b367ca0f2da18401a5dcca9ae69708dafb319a0f2f3158eecaaafd157720bf76f",
            "salt": "11470618636631188992448980835259862494560825989902152101415102057722156057653446316377871334408059259295477871909772111141208436623765633405097491079769148",
            "voted": False},
        "colelentini": {
            "hash": "d98d585c1e65313447ed91e22ae0ac238fa66794e58de0015e971d2afae52bd473729b2fa163ee7444f2daf93260b4e01ae898bc0ddd05ab0e7deef82ac0c4f0",
            "salt": "4474224011127718864367360795317029004273840252901266827352110545395019104677140338547586238487906388464847154944094665793056033201216940692650853568233924",
            "voted": False},
        }

    def user_exists(self, username):
        if username in self.database:
            return True
        else:
            return False

    def get_hash(self, username):
        return self.database[username]["hash"]

    def get_salt(self, username):
        return self.database[username]["salt"]

    def user_voted(self, username):
        return self.database[username]["voted"]

    def set_voted(self, username):
        self.database[username]["voted"] = True

database = Database()
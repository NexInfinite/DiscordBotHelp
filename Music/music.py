import discord
from discord.ext import commands
import pafy
import asyncio
import aiohttp


'''
Simple Music Bot made with Pafy and FFMPEG by Zeffo#9673 and Motzumoto#9773
'''

# Constants (remove these before sharing plis)
YOUTUBE_SEARCH_ENDPOINT = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={0}&type=video&key={1}'
YOUTUBE_SONG_URL = 'https://www.youtube.com/watch?v={0}'
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
SPOTIFY_CLIENT_ID = '00f2564d102142fbb5d9229533aede9e'
SPOTIFY_CLIENT_SECRET = 'dbdb32a313a047db851ff02448a9b6d3'



class Music(commands.Cog):
    """Listen to your favorite music with your friends!"""
    def __init__(self, bot):
        self.bot = bot
        self.queues = {} # Store a Queue for each guild
        self.bot.loop.create_task(self._self_deafen())
        self.session = aiohttp.ClientSession()
        self.yt_key = " "


    async def _self_deafen(self):
        tasks = [guild.me.edit(deafen=True) for guild in self.bot.guilds]
        await asyncio.gather(*tasks)


    def embed(self, p):
        e = discord.Embed(title=p.title, color=0x020202)
        e.add_field(name='Duration', value=f'`{p.duration}`')
        e.add_field(name='Views', value=f'`{p.viewcount}`', inline=False)
        e.add_field(name='Rating', value=f'`{p.rating}`', inline=False)
        e.set_thumbnail(url=p.thumb)
        e.set_author(name=str(p.req), icon_url=str(p.req.avatar_url))
        return e


    @commands.command(usage='`tp!play (song name | YouTube URL)`')
    async def play(self, ctx, *, song: str):
        '''A command that searches and plays audio from YouTube.'''
        if not ctx.author.voice:
            return await ctx.message.reply('You must be in a Voice Channel!', delete_after=5)
        elif ctx.guild.voice_client:
            q = self.queues.get(ctx.guild.id)
            item = await self._parse(song, ctx)
            if item:
                q.put(item)
                await ctx.message.reply(content='`Added to the queue!`', embed=self.embed(self.queues.get(ctx.guild.id).last()))
            else:
                await ctx.message.reply('Could not find the song...')
                return
            if not q.np and not q.empty():
                await self._handler(ctx)
        else:
            await ctx.author.voice.channel.connect()
            items = await self._parse(song, ctx)
            if items:
                q = Queue(id=ctx.guild.id, guild=ctx.guild)
                q.put(items)
                self.queues[ctx.guild.id] = q
                await self._handler(ctx)
            else:
                await ctx.message.reply('Could not find the song...')
                return

    @commands.command(usage='`tp!volume (0 to 1)`')
    async def volume(self, ctx, amount: float):
        '''A command that changes the bot volume.'''
        if vc := ctx.guild.voice_client:
            vc.source.volume = amount
            self.queues.get(ctx.guild.id).volume = amount

    @commands.command(usage='`tp!stop`')
    async def stop(self, ctx):
        '''A command that stops music playback. It erases the queue and disconnects the bot from the voice channel.'''
        if vc := ctx.guild.voice_client:
            await vc.disconnect()
            if ctx.guild.id in self.queues:
                del self.queues[ctx.guild.id]


    async def _parse(self, _input, ctx):
        '''parses user input and returns pafy object(s)'''
        if 'watch?' in _input:
            try:
                p = await self.run_async(pafy.new, _input)
            except:
                return None
            p.req = ctx.author
            return p
        elif 'playlist?' in _input:
            p = await self.run_async(pafy.get_playlist, _input)
            items =  [p['items'][i]['pafy'] for i in range(0, len(p['items']))]
            for i in items:
                i.req = ctx.author
            return items
        else:
            d = await self._get_data(_input)
            try:
                r = d["items"][0]["id"]["videoId"]
                p = await self.run_async(pafy.new, r)
            except:
                return None
            p.req = ctx.author
            return p

    def spotify_url_parser(self, input):
        '''Not to be impl'''
        remove_text = r'https://open.spotify.com/track/'
        n = input.replace(remove_text, '')
        r = n.split('?')
        print(r[0])
        return r[0]

    async def _play(self, ctx, url, volume):
        '''Helper subroutine that plays audio with the given data '''
        stream = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        transform_stream = discord.PCMVolumeTransformer(stream, volume)
        ctx.guild.voice_client.play(transform_stream, after=lambda x: self.bot.loop.create_task(self._handler(ctx)))


    async def _handler(self, ctx):
        '''Handles playing of songs'''
        queue = self.queues.get(ctx.guild.id)
        if not queue:
            return
        if queue.empty() and not queue.loop:
            queue.np = None
            await ctx.voice_client.disconnect()
        elif not queue.loop:
            song = (await self.run_async(queue.get().getbestaudio)).url_https
            await self._play(ctx, song, queue.volume)
            await ctx.message.reply(content='`Now playing:`', embed=self.embed(queue.np))
        elif queue.loop:
            song = (await self.run_async(queue.loop_get().getbestaudio)).url_https
            await self._play(ctx, song, queue.volume)


    async def _get_data(self, _input):
        '''YouTube Search'''
        response = await self.session.get(YOUTUBE_SEARCH_ENDPOINT.format(_input, self.yt_key))
        result = await response.json()
        return result


    def queue_embed(self, q):
        '''Helper function to create an instance of discord.Embed with the given data'''
        desc = '```md\n' + f'Now Playing: {q.np.title} (Requested by: {q.np.req})\n\n' + '\n'.join(f'{n}. {s.title} (Requested by: {s.req})' for n, s in enumerate(q.queue)) + '```'
        embed = discord.Embed(title='Queue', description=desc)
        embed.set_author(name=q.guild.name, icon_url=str(q.guild.icon_url))
        return embed

    @commands.command(usage='`tp!queue`')
    async def queue(self, ctx):
        '''A command that lists the music queue. '''
        if len((q := self.queues.get(ctx.guild.id)).queue) > 0:
            embed = self.queue_embed(q)
        else:
            embed = discord.Embed(title='The queue is empty.')
        await ctx.message.reply(embed=embed)

    async def run_async(self, coro, *args):
        return await self.bot.loop.run_in_executor(None, coro, *args)


    @commands.command(usage='`tp!remove (index)`')
    async def remove(self, ctx, element: int):
        '''A command that removes a song from the given index from the queue '''
        q = self.queues.get(ctx.guild.id)
        if not q:
            embed = discord.Embed(title='There is nothing playing!')
        elif element >= len(q.queue):
            embed = discord.Embed(title=f'There are only {len(q.queue)} songs playing!')
        else:
            q.queue.pop(element)
            embed = self.queue_embed(q)

        await ctx.message.reply(embed=embed)


    @commands.command(usage='`tp!skip`')
    async def skip(self, ctx):
        '''A command that skips the song that is currently playing and plays the next song in the queue. '''
        queue = self.queues.get(ctx.guild.id)
        vc = ctx.guild.voice_client
        #if queue.np.req.id == ctx.author.id:
        self._skip(ctx, queue, vc)
        await ctx.message.reply('Skipping immediately!')


    def _skip(self, ctx, queue, vc):
        '''Helper function to skip with the given data'''
        vc.stop()
        queue.loop = None


    @commands.command(usage='`tp!pause`')
    async def pause(self, ctx):
        '''A command that pauses the current song.'''
        if vc := ctx.voice_client:
            vc.pause()
            await ctx.send("Song paused.")


    @commands.command(usage='`tp!resume`')
    async def resume(self, ctx):
        '''A command that resumes the current song. '''
        if vc := ctx.voice_client:
            vc.resume()
            await ctx.send("Song resumed.")


    @commands.command(aliases=['np'], usage='`tp!nowplaying/np`')
    async def nowplaying(self, ctx):
        '''A command that displays the song which is currently playing. '''
        q = self.queues.get(ctx.guild.id)
        if q and q.np:
            await ctx.message.reply(embed=self.embed(q.np))
        else:
            await ctx.message.reply('`No songs are currently playing! Use ♫play (song) to play a song from YouTube in your voice channel.``')


    @commands.command(usage='`tp!loop`')
    async def loop(self, ctx):
        '''A command which loops the currently playing song and the songs in the queue. '''
        if queue := self.queues.get(ctx.guild.id):
            if not queue.loop:
                queue.loop = queue.queue + [queue.np]
                await ctx.message.reply(content='`Looping!`', embed=self.embed(queue.np))
            else:
                queue.loop = []
                await ctx.message.reply('`Stopping loop!`')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        ''' Handle the unfortunate event in which the bot is kicked from a vc. Delete queue and cleanup'''
        if member != self.bot.user: return
        if before.channel and not after.channel and self.queues.get(member.guild.id):
            self.queues.pop(member.guild.id, None)


# Refactor with asyncio.Queue when possible
class Queue:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.guild = kwargs['guild']
        if args:
            self.queue = [arg for arg in args]
            self.np = self.queue[0]
        else:
            self.queue = []
            self.np = None
        self.loop = []
        self.loop_index = 0
        self.volume = 0.1


    def put(self, item):
        # print(item)
        if isinstance(item, list):
            self.queue.extend(item)
        else:
            self.queue.append(item)

    def get(self):
        t = self.queue.pop(0)
        self.np = t
        return t

    @property
    def titles(self):
        return [i.title for i in self.queue]

    @property
    def urls(self):
        return [i.getbestaudio().url_https for i in self.queue]


    def put_playlist(self, p):
        for item in p['items']:
            self.queue.append(item['pafy'])


    def empty(self):
        return len(self.queue) == 0


    def last(self):
        if self.empty():
            return self.np
        else:
            return self.queue[len(self.queue)-1]


    def loop_get(self):
        # print('DEBUGGING', len(self.loop), self.loop_index)
        song = self.loop[self.loop_index]
        self.np = song
        # print(song, self.loop_index, self.loop)
        if len(self.loop)-1 == self.loop_index:
            self.loop_index = 0
        elif len(self.loop) > self.loop_index:
            self.loop_index += 1
        else:
            print(len(self.loop), self.loop_index)
        return song



def setup(bot):
    bot.add_cog(Music(bot))
